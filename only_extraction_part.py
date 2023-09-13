import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2
from os_operations import folder_path, files, move_file
import logging
import numpy as np


logging.basicConfig(filename="logs.log",filemode="w", level=10, format="%(asctime)s:%(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

def pdf_to_image_to_text(pdf_path,file_name,row_number, dpi=1100, contrast_factor=1.5, sharpness_factor=1.7, clarity_factor=1.7):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    Total_Extracted_Text = ""

    title_flag = None

    logging.info(f"started reading {file_name}....")
    # Iterate through the pages and save them as images with the specified DPI
    for page_number in range(pdf_document.page_count):
        # if page_number<3:
        page = pdf_document.load_page(page_number)
        logger.info(f"Converted {page_number+1} to image")
        print(f"Converted {page_number+1} to image")
        logger.info(f"Enhancing Image Quality for page {page_number + 1}...")
        print(f"Enhancing Image Quality for page {page_number + 1}...")
        image = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        print("Adjusting Image Area...")
    
        # Convert to a Pillow image
        image = Image.frombytes("RGB", [image.width, image.height], image.samples)
        print("Still need more Clearity")
    
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast_factor)
        print("Adjusting Sharpness in image.....")
    
        # Enhance sharpness
        image = image.filter(ImageFilter.SHARPEN)
    
        # Enhance clarity
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(clarity_factor)
        logger.info("image processed successfully....")
        print("image processed successfully....")
        processed_image = np.array(image)
        gray_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
    
        # Configure Tesseract for more accuracy
        # thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # custom_config = r'--oem 3 --psm 6'  # Adjust PSM and OEM as needed
        # extracted_text = pytesseract.image_to_string(thresh, config=custom_config, lang='eng')
    
    
        # Apply OCR to extract text from the scanned image
        logger.info("Extracting Text from converted image using AI Tools...")
        print("Extracting Text from converted image using AI Tools...")
        extracted_text = pytesseract.image_to_string(gray_image)
    
        Total_Extracted_Text+=f"******************************page{page_number+1}*************************************"
        Total_Extracted_Text += "\n"
        Total_Extracted_Text+=extracted_text
        Total_Extracted_Text+="\n"
    
    
        logger.info(f"Text Extracted Successfully from Page {page_number}......")
    pdf_document.close()
    # title validation
    if len(Total_Extracted_Text)>100:
        store_extracted_data = open(f"extracted_data_in_text_format\\{file_name[:-4]}.txt", "w+")
        store_extracted_data.write(Total_Extracted_Text)
        store_extracted_data.close()
    

if __name__ == "__main__":
    row_number = 1
    for file_name in files:
        row_number += 1
        pdf_file = f"{folder_path}\\{file_name}"
        pdf_to_image_to_text(pdf_file, file_name, row_number)
        move_file(pdf_file,"converted_files")