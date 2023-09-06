import fitz  # PyMuPDF
import pytesseract
from os_operations import folder_path, files, move_file
from pysite import extract_text_from_pdf
from parameters_validation import title_validation
from update_excel_sheet import worksheet, workbook
from table_fetching import fetch_table_data, gst_validation

row_number = 2

# Path to the PDF file you want to extract text from
for file in files:
    source_path = f"{folder_path}\\{file}"
    destination = "filter1\\"

    fetch_table_data(source_path)

    # Initialize the PyMuPDF PDF document
    pdf_document = fitz.open(source_path)

    # Initialize Tesseract OCR
    # Update with your Tesseract installation path
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Initialize a variable to store the extracted text
    extracted_text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        # Extract the text from the current page using PyMuPDF's get_text
        page_text = page.get_text()
        # Append the extracted text to the overall text
        extracted_text += page_text

    # Close the PDF document
    pdf_document.close()



    #filter 1 application
    title_validation_status = title_validation(extracted_text)
    extracted_text_via_pysite = extract_text_from_pdf(source_path)
    # title_validation_status_via_pysite = title_validation(extracted_text_via_pysite)

    if title_validation_status[0] == 1:
        print(f"*****************************************{source_path}*****************************************")
        move_file(source_path, destination)

        row_number += 1
        gst_number = gst_validation(title_validation_status[1])
        worksheet[f"A{row_number}"] = file
        worksheet[f"S{row_number}"] = ",\n".join([i for i in (set(gst_number))])
        workbook.save("source.xlsx")

    elif len(extracted_text_via_pysite) != 0:
        print(f"******************************** pysite {source_path}*****************************************")
        move_file(source_path, destination)
        row_number += 1
        gst_number = gst_validation(extracted_text_via_pysite)
        worksheet[f"A{row_number}"] = file
        worksheet[f"S{row_number}"] = ",\n".join([i for i in (set(gst_number))])
        workbook.save("source.xlsx")
        workbook.close()



else:
    print("not able to fetch invoice data")




