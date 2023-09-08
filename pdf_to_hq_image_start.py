import fitz  # PyMuPDF
import logging
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2
import numpy as np
from update_excel_sheet import workbook, worksheet
from os_operations import folder_path, files, move_file

#
logging.basicConfig(filename="logs.log",filemode="w", level=10, format="%(asctime)s:%(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


from parameter_validations import Extracted_Data_Validations
def pdf_to_images(pdf_path,file_name,row_number, dpi=600, contrast_factor=1.5, sharpness_factor=2.0, clarity_factor=1.5):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    destination = "data_extraction_pass"
    Total_extracted_data_len = 0

    title_flag = "Not Available"
    worksheet[f"A{row_number}"] = row_number-1
    worksheet[f"B{row_number}"] = file_name
    worksheet[f"C{row_number}"] = title_flag

    logging.info(f"started reading {file_name}....")
    print("started reading", file_name)
    # Iterate through the pages and save them as images with the specified DPI
    for page_number in range(pdf_document.page_count):
        logger.info(f"Reading page {page_number+1} / {pdf_document.page_count}...")
        print(f"Reading page {page_number+1} / {pdf_document.page_count}...")
        page = pdf_document.load_page(page_number)
        logger.info(f"Converted {page_number + 1} to image")
        print(f"Converted {page_number + 1} to image")
        logger.info("Enhancing Image Quality for page [page_number + 1}...")
        print("Enhancing Image Quality for page [page_number + 1}...")
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

        # Apply OCR to extract text from the scanned image
        logger.info("Extracting Text from converted image using AI Tools...")
        print("Extracting Text from converted image using AI Tools...")
        extracted_text = pytesseract.image_to_string(gray_image)
        Total_extracted_data_len+= len(extracted_text)


        logger.info(f"Text Extracted Successfully from Page {page_number}......")
        print("Extracting Text from converted image using AI Tools...")

        # print(extracted_text)

        #title validation
        if title_flag == "Not Available":
            logger.info(f"Checking title availability on {page_number+1}//{pdf_document.page_count}...")
            print(f"Checking title availability on {page_number+1}//{pdf_document.page_count}...")
            tax_invoice_title = ["Tax Invoice", "TAX INVOICE", "tax invoice"]

            for title_assumption in tax_invoice_title:
                if title_assumption in extracted_text:
                    print(f"{title_assumption} is present in Extracted Data page number {page_number+1}")
                    title_flag = "Available"
                    worksheet[f"C{row_number}"] = f"{title_assumption} on page {page_number+1}"

                    # Verify_Data = Extracted_Data_Validations(data=extracted_text)
                    # Gst_Data = Verify_Data.gst_validation()
                    # identity_validated_data = Verify_Data.Identity_Segregation()
                    #
                    # #CONSIGNEE DATA FILLING
                    # print("Filling Consignee gst details")
                    # worksheet[f"E{row_number}"] = identity_validated_data["CONSIGNEE"]["GSTN"]
                    # worksheet[f"F{row_number}"] = identity_validated_data["CONSIGNEE"]["GSTN_STATUS"]
                    #
                    #
                    # #CONSIGNER DATA FEELING
                    # print("Filling Consignor details")
                    # worksheet[f"G{row_number}"] = identity_validated_data["CONSIGNOR"]["GSTN"]
                    # worksheet[f"H{row_number}"] = identity_validated_data["CONSIGNOR"]["GSTN_STATUS"]
                    # workbook.save("source.xlsx")




                    # print(f"**********************************{Gst_Data}*****************************************")
                    # print(f"**********************************{Verify_Data.Identity_Segregation()}*****************************************")




            # GST Validation Extraction

            # print(fetch_gst_number)



            # PO Number


            #invoice number


            #consignee details
                # consignee name

                # consignee state and state code


            #consigner details
                # consigner name

                # consigner state and state code








    # Close the PDF file
    pdf_document.close()
    if Total_extracted_data_len >50:
        Verify_Data = Extracted_Data_Validations(data=extracted_text)
        Gst_Data = Verify_Data.gst_validation()
        identity_validated_data = Verify_Data.Identity_Segregation()

        # CONSIGNEE DATA FILLING
        print("Filling Consignee gst details")

        if "GSTN" in identity_validated_data["CONSIGNEE"]:
            worksheet[f"E{row_number}"] = identity_validated_data["CONSIGNEE"]["GSTN"]
            worksheet[f"F{row_number}"] = identity_validated_data["CONSIGNEE"]["GSTN_STATUS"]
        else:
            worksheet[f"E{row_number}"] = "GST Number Not Available"
            worksheet[f"F{row_number}"] = None


        # CONSIGNER DATA FEELING
        print("Filling Consignor details")
        if "GSTN" in identity_validated_data["CONSIGNOR"]:
            worksheet[f"G{row_number}"] = identity_validated_data["CONSIGNOR"]["GSTN"]
            worksheet[f"H{row_number}"] = identity_validated_data["CONSIGNOR"]["GSTN_STATUS"]
        else:
            worksheet[f"E{row_number}"] = "GST Number Not Available"
            worksheet[f"F{row_number}"] = None
        workbook.save("source.xlsx")
        move_file(pdf_path, destination)
    else:
        move_file(pdf_path, "data_extraction_fail\\")


if __name__ == "__main__":
    row_number = 1
    for file_name in files:
        row_number += 1
        pdf_file = f"{folder_path}\\{file_name}"
        # output_folder = "word_data"
        pdf_to_images(pdf_file, file_name, row_number)
        workbook.close()