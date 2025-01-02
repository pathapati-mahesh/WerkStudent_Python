# DataExtraction Documentation

## Overview

The purpose of the `DataExtraction` class is to extract data from PDF invoice files, transform it into `DataFrame`, and export the output to CSV and Excel files.

## Features

- Extracts data from invoice PDFs using `tabula` and `PyPDF2`.
- Processes invoice details like total amount and invoice date.
- Output data as Pandas DataFrames.
- Exports the results into Excel and CSV formats.

## Requirements

Make sure the following Python libraries are installed and also Java8 or more is installed in your System

- `distro==1.9.0`
- `et_xmlfile==2.0.0`
- `numpy==2.2.1`
- `openpyxl==3.1.5`
- `pandas==2.2.3`
- `pip==24.3.1`
- `PyPDF2==3.0.1`
- `python-dateutil==2.9.0`
- `pytz==2024.2`
- `setuptools==63.2.0`
- `six==1.17.0`
- `tabula==1.0.5`
- `tabula-py==2.10.0`
- `tabulate==0.9.0`
- `tzdata==2024.2`
  You can install above libraries using pip:

```bash
pip install -r requirements.txt
```

## Class Methods
- **In the Folder you will find the Class Methods in `script.py` file**
### Constructor

```python
__init__(**kwargs)
```

- **Parameters:**
  - `invoice_pdf1`: Path to the first invoice PDF file.
  - `invoice_pdf2`: Path to the second invoice PDF file.
- **Description:** Initializes the class with PDF file paths.

### get_connection_str(path, file_name)

- **Parameters:**
  - `path`: Absolute path of the invoice PDF.
  - `file_name`: Name of the invoice PDF.
- **Description:** Reads the PDF file using `tabula` (for structured PDFs) or `PyPDF2` (for text extraction).
- **Returns:** List of DataFrames or a `PdfReader` object.

### get_filename(invoice_file_name)

- **Parameters:**
  - `invoice_file_name`: Path to the PDF file.
- **Description:** Extracts the file name without the extension.
- **Returns:** File name as a string.

### get_absfile_path(invoice_file_name)

- **Parameters:**
  - `invoice_file_name`: Path to the PDF file.
- **Description:** Returns the absolute path of the file.
- **Returns:** Absolute file path as a string.

### convert_date(format_type, date_time)

- **Parameters:**
  - `format_type`: Either 'German' or 'No'.
  - `date_time`: Date string to be formatted.
- **Description:** Converts date formats into `dd-MMMM-yyyy`.
- **Returns:** Formatted date string.

### format_invoice2(abs_filePath, abs_fileName)

- **Parameters:**
  - `abs_filePath`: Absolute path of the invoice file.
  - `abs_fileName`: invoice File name.
- **Description:** Extracts `Total USD` and `Invoice Date` from invoice pdf2 and returns a DataFrame.
- **Returns:** Pandas DataFrame consists of `File Name`, `Date`, and `Value`.

### get_data()

- **Description:** Extracts data from both invoice PDFs, merges them into a single DataFrame, and saves results to Excel and CSV files. Created One excel file with two sheets in it. One sheet has the Raw info from pdf1 and pdf2. Other sheet has Pivot table of pdf1 and pdf2. Csv file has the Raw data
- **Returns:** Merged DataFrame with `File Name`, `Date`, and `Value`.

## Usage Example

```python


if __name__ == '__main__':
    invoice_file_name1 = "sample_invoice_1.pdf"
    invoice_file_name2 = "sample_invoice_2.pdf"
    extract_data = DataExtraction(invoice_pdf1=invoice_file_name1, invoice_pdf2=invoice_file_name2)
    extract_data.get_data()
```

## Outputs

In `Output` folder you will find the created Excel, csv files.

- **Excel File:** `invoice_excel.xlsx`
  - Sheet 1: Raw data from both PDFs.
  - Sheet 2: Pivot table summarizing the data.
- **CSV File:** `Total.csv` (semicolon-separated).

## Executable File

- Yet to Create

## Author

**P Mahesh Kumar**
