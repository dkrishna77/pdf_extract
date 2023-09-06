import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from docx import Document
from parameter_validations import check_text_in_first_half
import numpy as np



def pdf_to_images(pdf_path, image_folder, dpi=600, contrast_factor=1.5, sharpness_factor=2.0, clarity_factor=1.5):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

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
        print("type", type(processed_image))
        
        
        tax_invoice_title =["Tax Invoice", "TAX INVOICE", "tax invoice"]
        for title_assumption in tax_invoice_title:
            title_val = check_text_in_first_half(processed_image, title_assumption)
            print(title_val)

        extracted_text = pytesseract.image_to_string(image, lang='eng')  # You can specify the language as needed

    # Create a new Word document
        doc = Document()

    # Add the extracted text to the Word document
        doc.add_paragraph(extracted_text)

        # Save the image
        doc.save(f"{image_folder}/page_{page_number + 1}.docx")

    # Close the PDF file
    pdf_document.close()

if __name__ == "__main__":
    pdf_file = "sample_pdf\\0.pdf"
    output_folder = "word_data"

    pdf_to_images(pdf_file, output_folder)
