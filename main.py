import locale
locale.setlocale(locale.LC_TIME, 'deu')



if __name__ == "__main__":
    invoice_file_name1 = "sample_invoice_1.pdf"
    invoice_file_name2 = "sample_invoice_2.pdf"
    
    from extraction_script.script import DataExtraction
    from extraction_script.install_req_script import VirtualEnv

    obj = VirtualEnv(requirements_file="requirements.txt")
    check = obj.install_requirements()
    
    extract_data = DataExtraction(invoice_pdf1=invoice_file_name1, invoice_pdf2=invoice_file_name2)
    extract_data.get_data()
