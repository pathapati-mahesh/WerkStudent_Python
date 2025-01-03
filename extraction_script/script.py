import os
import datetime
import locale
import pandas as pd
import tabula
from PyPDF2 import PdfReader
# Used locale to set system DateTime to German timezone
locale.setlocale(locale.LC_TIME, 'deu')

class  DataExtraction:
    
    """
    This Class is used to extract the Data from  Invoices and also 
    writes the data in to Dataframes, excel and csv files.
    """
    def __init__(_self,**kwargs):
        _self.file_name = None
        _self.invoice_details=dict(kwargs)
        _self.invoice_file1=_self.invoice_details.get('invoice_pdf1')
        _self.invoice_file2=_self.invoice_details.get('invoice_pdf2')
        _self.requirements_file=_self.invoice_details.get('requirements_file')
        
    
    def get_connection_str(_self,path,file_name):
        """In this method I used modules to read
            the pdf that are mentioned in the task. As there is some Data loss in case of tabulate for 2nd pdf.
            So I used 'PyPDF2' to read the 2nd invoice pdf. Following code snippet returns the List[DatFrames] and Pypdf
            return the text
        """
        conn_str=None
        if file_name=="sample_invoice_1":
            
            conn_str=tabula.read_pdf(path,pages="all",multiple_tables=True)
        if file_name=="sample_invoice_2":
            
            conn_str=PdfReader(path)
        return conn_str


    def get_filename(_self,invoice_file_name):
        """Useful to extract the file name without extension"""
        _self.file_name = os.path.basename(invoice_file_name).split('.')[0]
        return _self.file_name
    
    
    def get_absfile_path(_self,invoice_file_name):
        """Useful to extract the Absolute path of the invoice_file"""
        get_path=os.path.dirname(os.path.abspath(invoice_file_name))
        abs_path=f"{str(get_path)}\\{str(invoice_file_name)}"
        return abs_path
    
    
    @staticmethod
    def convert_date(format_type,date_time):

        """In sample_invoice_1.pdf,sample_invoice_2.pdf 
        the Date format is different converting the date in both the
        pdf in to common format which is 'Date-Month-YYYY' format
        """

        if format_type=='German':
            date_obj = datetime.datetime.strptime(date_time.replace(',', ''), '%d %B %Y')
        else:
            date_obj = datetime.datetime.strptime(date_time.replace('.', ' '), '%b %d %Y')
        date= date_obj.strftime('%d-%B-%Y')
        return date
    
    
    def format_invoice2(_self,abs_filepath,abs_filename):
       
        """Integrated line by Line and checked whether the Total USD and
        Invoice Date is there or not and Assigned it to the  respective variables and this method 
        returns the Dataframe with 'File Name','Date','Value(Amount)'
        """
        total_amount = None
        invoice_date=None
        reader = _self.get_connection_str(path=abs_filepath,file_name=abs_filename)
        """Iterate through the pages to find 'Total USD' and 'Invoice date' """
        for page in reader.pages:
            text = page.extract_text()
            if "Total USD" and "Invoice date" in text:
                for line in text.split("\n"):
                    """Formatting the Invoice Date """
                    if "Invoice date" in line:
                        invoice_date=line.replace("Invoice date:", "Invoice_date=")
                    if "Total USD" in line:
                        """Formatting the Total USD """
                        total_amount = line.replace("Total USD", "Total = USD")
                        break
            
            if total_amount and invoice_date:
                break
        if total_amount and invoice_date:
            date=invoice_date.split('=')[1].strip().replace(',','')
            format_date=DataExtraction.convert_date("No",date)
            total_amount=f"{total_amount.split('= USD $')[1].strip()} $"
            # Created New dataframe according to the Requirements for the Task
            data_df=pd.DataFrame({
                                "File Name":[abs_filename],
                                "Date":[format_date],
                                "Value":[total_amount]
                            })
            return data_df
        else:
            return None
    

    
    def get_data(_self):
        
        """In this Method Extracted te desired Dataframes from both the files and transforming the data from pdf1 and pdf2
        returns the Dataframe including information like 'File Name','Date','Value' """

        abs_path=_self.get_absfile_path(_self.invoice_file1)
        file_name=_self.get_filename(_self.invoice_file1)
        df = _self.get_connection_str(path=abs_path,file_name=file_name)
        invoice_date=str(df[0]['Date'][0]).replace('.', ' ')
        format_date=DataExtraction.convert_date(format_type="German",date_time=invoice_date)

        "Extracting the Required Dataframe from the analysed PDF "
        get_invoice_df = df[1]
        get_invoice_df.rename(columns={"Amount\r-without VAT-":"Amount_without_VAT"},inplace=True)
        gross_amount_df = get_invoice_df[get_invoice_df['Service Description']=='Gross Amount incl. VAT'].reset_index()
        gross_amount=gross_amount_df["Amount_without_VAT"][0]
        pdf1_invoice=pd.DataFrame({
                        "File Name":[file_name],
                        "Date":[format_date],
                        "Value":[gross_amount]
                     })
        print("------------------Printing Dataframe of sample invoice pdf1--------")
        print(pdf1_invoice)
        abs_filepath=_self.get_absfile_path(invoice_file_name=_self.invoice_file2)
        abs_filename=_self.get_filename(_self.invoice_file2)
        pdf2_invoice=_self.format_invoice2(abs_filepath,abs_filename)
        print("------------------Printing Dataframe of sample invoice pdf2--------")
        print(pdf2_invoice)
        merged_df=pd.concat([pdf1_invoice,pdf2_invoice],axis=0,ignore_index=True)
        print("------------------Printing the Merged Dataframe--------------------")
        print(merged_df)

        """ Writes the merged Dataframe in to Excel file in to Two Different sheets(invoice_1,invoice_2)
            Also, Creates a csv file with the Merged DataFrame.
        """
        with pd.ExcelWriter('output_invoice.xlsx') as writer:
            merged_df.to_excel(writer, sheet_name='invoice_1', index=False)
            pivot_table = merged_df.pivot_table(index=['File Name'],
                       values=['Value'],
                       aggfunc='sum')
            pivot_table.to_excel(writer, sheet_name='invoice_2')
        merged_df.to_csv("output_invoice.csv",sep=';')

        return merged_df