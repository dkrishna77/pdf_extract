import fitz  # PyMuPDF
import logging
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2
import numpy as np
from update_excel_sheet import workbook, worksheet
from os_operations import folder_path, files, move_file
from parameter_validations import Extracted_Data_Validations


#logging configuration
logging.basicConfig(filename="logs.log",filemode="w", level=10, format="%(asctime)s:%(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

def pdf_to_image_to_text(pdf_path,file_name,row_number, dpi=600, contrast_factor=1.5, sharpness_factor=1.5, clarity_factor=1.7):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    # pdf_document = open(f"extracted_data\\{file_name[:-4]}.txt")
    destination = "data_extraction_pass\\"

    Total_Extracted_Text = ""
    # Total_Extracted_Text = pdf_document.read()

    title_flag = "Not Available"
    worksheet[f"A{row_number}"] = row_number-1
    worksheet[f"B{row_number}"] = file_name
    worksheet[f"C{row_number}"] = title_flag
    workbook.save("source.xlsx")

    logging.info(f"started reading {file_name}....")
    print("started reading", file_name)
    # Iterate through the pages and save them as images with the specified DPI
    for page_number in range(pdf_document.page_count):
    
        logger.info(f"Reading page {page_number+1} / {pdf_document.page_count}...")
        print(f"Reading page {page_number+1} / {pdf_document.page_count}...")
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
    
        # Configure Tesseract
        # thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # custom_config = r'--oem 3 --psm 6'  # Adjust PSM and OEM as needed
    
        # Perform OCR
    
        # Apply OCR to extract text from the scanned image
        logger.info("Extracting Text from converted image using AI Tools...")
        print("Extracting Text from converted image using AI Tools...")
        # extracted_text = pytesseract.image_to_string(thresh, config=custom_config, lang='eng')
        extracted_text = pytesseract.image_to_string(gray_image)
    
        Total_Extracted_Text+=f"******************************page{page_number+1}*************************************"
        Total_Extracted_Text += "\n"
        Total_Extracted_Text+=extracted_text
        Total_Extracted_Text+="\n"
    
    
        logger.info(f"Text Extracted Successfully from Page {page_number}......")
        print("Extracting Text from converted image using AI Tools...")
    store_extracted_data = open(f"extracted_data\\{file_name[:-4]}.txt", "w")
    store_extracted_data.write(Total_Extracted_Text)
    store_extracted_data.close()
    
    
    logger.info(f"Checking title availability on {page_number + 1}//{pdf_document.page_count}...")
    print(f"Checking title availability on {page_number + 1}//{pdf_document.page_count}...")

    # title validation

    tax_invoice_title = ["Tax Invoice", "TAX INVOICE", "tax invoice"]

    for title_assumption in tax_invoice_title:
        if title_flag == "Not Available" and title_assumption in Total_Extracted_Text:
            print(f"{title_assumption} is present in Extracted Data")
            title_flag = "Available"
            worksheet[f"C{row_number}"] = f"{title_assumption} is present"
            workbook.save("source.xlsx")



    Verify_Data = Extracted_Data_Validations(data=Total_Extracted_Text,row_number=row_number)
    Gst_Data = Verify_Data.gst_validation()
    Gst_validated_data = Verify_Data.Gst_Segragation()
    State_validated_data = Verify_Data.State_Segragation()
    Po_Number_validated_data = Verify_Data.PO_Number_Identifier()
    Invoice_number_validated_data = Verify_Data.Inv_Num_Identifier()
    print(f"*********************************************************fetched data{Invoice_number_validated_data}***************************************************************************************")

    #CONSIGNEE DATA FILLING
    print("Filling Consignee gst details")
    if "GSTN" in Gst_validated_data["CONSIGNEE"]:
        # pass
        worksheet[f"E{row_number}"] = Gst_validated_data["CONSIGNEE"]["GSTN"]
    #
    #
    # # CONSIGNER DATA FEELING
    # print("Filling Consignor details")
    if "GSTN" in Gst_validated_data["CONSIGNOR"]:
        # pass
        worksheet[f"F{row_number}"] = Gst_validated_data["CONSIGNOR"]["GSTN"]
    # worksheet[f"H{row_number}"] = identity_validated_data["CONSIGNOR"]["GSTN_STATUS"]
    workbook.save("source.xlsx")

    # move_file(pdf_path, destination)

    # else:
    #     move_file(pdf_path, "data_extraction_fail")
    #     # Close the PDF file
    Invoice_number_validated_data = {}
    pdf_document.close()





if __name__ == "__main__":
    row_number = 1
    for file_name in files:
        row_number += 1
        pdf_file = f"{folder_path}\\{file_name}"
        result = pdf_to_image_to_text(pdf_file, file_name, row_number)
        print(result)
    workbook.close()