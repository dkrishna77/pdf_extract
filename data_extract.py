import fitz  # PyMuPDF
from PIL import Image
import pytesseract

import tabula
def pdf_to_images(pdf_file):
    doc = fitz.open(pdf_file)
    images = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap()
        images.append(pix)

    return images

def extract_text_from_image(image):
    image = Image.frombytes("RGB", [image.width, image.height], image.samples)
    pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\tessdata"
    text = pytesseract.image_to_string(image)
    return text


def main(pdf_file):
    images = pdf_to_images(pdf_file)

    for i, image in enumerate(images):
        text = extract_text_from_image(image)
        print(f"Page {i + 1} Text:")
        print(text)



if __name__ == "__main__":
    pdf_file = "sample_pdf\\0.pdf"
    main(pdf_file)
