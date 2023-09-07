import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2
# from docx import Document
import numpy as np
from update_excel_sheet import workbook, worksheet
from os_operations import folder_path, files, move_file
def pdf_to_images(pdf_path,file_name,row_number, dpi=600, contrast_factor=1.5, sharpness_factor=2.0, clarity_factor=1.5):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    destination = "title_check_pass"

    title_flag = "Not Available"
    worksheet[f"A{row_number}"] = row_number-1
    worksheet[f"B{row_number}"] = file_name
    worksheet[f"C{row_number}"] = title_flag


    # Iterate through the pages and save them as images with the specified DPI
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))

        # Convert to a Pillow image
        image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast_factor)

        # Enhance sharpness
        image = image.filter(ImageFilter.SHARPEN)

        # Enhance clarity
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(clarity_factor)

        processed_image = np.array(image)
        gray_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)

        # Apply OCR to extract text from the scanned image
        extracted_text = pytesseract.image_to_string(gray_image)
        # print(extracted_text)

        #title validation
        if title_flag == "Not Available":
            tax_invoice_title = ["Tax Invoice", "TAX INVOICE", "tax invoice"]
            for title_assumption in tax_invoice_title:
                if title_assumption in extracted_text:
                    print(f"{title_assumption} is present in Extracted Data page number {page_number}")
                    title_flag = 1
                    worksheet[f"C{row_number}"] = title_assumption

                    workbook.save("source.xlsx")

        #GST Validation Extraction



    # Close the PDF file
    pdf_document.close()
    move_file(pdf_path, destination)


if __name__ == "__main__":
    row_number = 1
    for file_name in files:
        row_number += 1
        pdf_file = f"{folder_path}\\{file_name}"
        # output_folder = "word_data"
        pdf_to_images(pdf_file, file_name, row_number)
        workbook.close()