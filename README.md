# DataExtraction Documentation

## Overview

The purpose of the `DataExtraction` class is to extract data from PDF invoice files, transform it into `DataFrame`, and export the output to CSV and Excel files. Additionally, a new `VirtualEnv` class has been introduced to automate the installation of required packages and Java dependencies.

## Features

- Extracts data from invoice PDFs using `tabula` and `PyPDF2`.
- Processes invoice details like total amount and invoice date.
- Output data as Pandas DataFrames.
- Exports results into Excel and CSV formats.
- New feature to automatically install required packages and Java using the `install_req_script.py`.

## How to Create Virtual Environment and How to Activate it?

- **Automated Virtual Environment Setup:**

  - `install_req_script.py` automatically installs the required dependencies and Java (if missing) to run the script.
  - Virtual environment creation and dependency installation is handled within the script, removing the need for manual setup.

- **Java Installation:**
  - If Java is not installed, the script will attempt to install the latest version of Java using `winget`.
- **Locale Handling:**

  - The script now ensures that the system's locale is set to 'German' to correctly parse dates in the invoices.

- Process for Creating virtual Environment through **Command Prompt**

```cmd
python -m venv name_of_virtual_env
```

- **Activating** Virtual Environment from **cmd**
- **For Windows**
  ```
  .\name_env\Scripts\Activate
  ```
- **For Linux/Mac**

  ```
  source name_env\bin\activate

  ```

  `

## Requirements

Make sure the following Python libraries are installed and also Java8 or more is installed in your System

- `distro`
- `et_xmlfile`
- `numpy`
- `openpyxl`
- `pandas`
- `pip`
- `PyPDF2`
- `python-dateutil`
- `pytz`
- `setuptools`
- `six`
- `tabula`
- `tabula-py`
- `tabulate`
- `tzdata`
  You can install above libraries using pip:

```bash
pip install -r requirements.txt
```

- **Note :** You are no longer need to write the commands to install the requirements file`(VirtualEnv)`. Now I integrated the script to automatically install and run the **DATA EXTRACTION** script. You just have to run the `main.py` file to get the Output.

## Class Methods(VirtualEnv):

- **In the directory you will find the `VirtualEnv Class` in `extraction_script\install_req_script.py` file**

### Constructor

```python
__init__(**kwargs)
```

- **Parameters:**
  - `requirements_file`: : The path to the requirements.txt file.
- **Description:** Initializes the class with requirements_file path which will be useful to install the packages/modules that are used in the `script`.

### Methods

- `install_java():` Install's Java if not already installed.
- `upgrade_pip():` Upgrades pip to the latest version. If the python environment is <=3.10.3 then the pip version is 22 which is uncompatable for the packages that we are using. So for that reason we are upgrading the pip to version 24.
- `install_requirements():` After all this method install the required dependencies from requirements.txt file.

## Class Methods(Data Extraction)

- **In the directory you will find the `Data Extraction Class` in `extraction_script\script.py` file**

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

```

## Outputs

In `Output` folder you will find the created Excel, csv files.

- **Excel File:** `output_invoice.xlsx`
  - Sheet 1: Raw data from both PDFs.
  - Sheet 2: Pivot table summarizing the data.
- **CSV File:** `output_invoice.csv` (semicolon-separated).

## Executable File

- I created and tried executing it is giving me Java path error for tabula module. I have the Java installed in my system. As of now trying to resolve the issue im facing related to tabula-java
- I Used `pyinstaller` to create the .exe file of my Python Script`(main.py)`.
- Verify locale settings (`deu`) for proper date parsing.

### Command to Create the .exe file

```
pyinstaller --onefile --add-data "extraction_script;extraction_script" --add-data "requirements.txt;." --add-data "sample_invoice_1.pdf;." --add-data "sample_invoice_2.pdf;." main.py
```

- Facing some package related issues while creating the .exe file resolved all those package related issues. .exe is not executing as expected the code is breaking some where it is not showing anything in the logs also tried debugging the code.

## Author

**P Mahesh Kumar**
