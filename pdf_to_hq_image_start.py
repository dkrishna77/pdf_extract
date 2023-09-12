# import start
import fitz  # PyMuPDF
import logging
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2
import numpy as np
from os_operations import folder_path, files, move_file
import pandas as pd
import re
import pandas as pd
columns=['SrNo', 'File_Name', 'Title', 'PO_Number', 'Original_For_Recipient',
       'Tax_Invoice_Number', 'Consignor', 'Consignor_GST_No',
       'Consignor_State_Code', 'Consignor_State_Name', 'HSN/SAC', 'Consignee',
       'Consignee_GST_No', 'Consignee_State_Code', 'Consignee_State_Name',
       'Vehicle_Number', 'RCM_Status']

df = pd.DataFrame(columns=columns)

#logging configuration
# logging.basicConfig(filename="logs.log",filemode="w", level=10, format="%(asctime)s:%(message)s", datefmt="%H:%M:%S")
# logger = logging.getLogger(__name__)
#
def pdf_to_image_to_text(pdf_path,file_name, row_number, dpi=1200, contrast_factor=2.0, sharpness_factor=1.5, clarity_factor=2.0):
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)
#     Total_Extracted_Text = ""
    title_flag = None
#
#     logging.info(f"started reading {file_name}....")
#     # Iterate through the pages and save them as images with the specified DPI
#     for page_number in range(pdf_document.page_count):
#         # if page_number<3:
#         logger.info(f"Reading page {page_number+1} / {pdf_document.page_count}...")
#         print(f"Reading page {page_number+1} / {pdf_document.page_count}...")
#         page = pdf_document.load_page(page_number)
#         logger.info(f"Converted {page_number+1} to image")
#         print(f"Converted {page_number+1} to image")
#         logger.info(f"Enhancing Image Quality for page {page_number + 1}...")
#         print(f"Enhancing Image Quality for page {page_number + 1}...")
#         image = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
#         print("Adjusting Image Area...")
#
#         # Convert to a Pillow image
#         image = Image.frombytes("RGB", [image.width, image.height], image.samples)
#         print("Still need more Clearity")
#
#         # Enhance contrast
#         enhancer = ImageEnhance.Contrast(image)
#         image = enhancer.enhance(contrast_factor)
#         print("Adjusting Sharpness in image.....")
#
#         # Enhance sharpness
#         image = image.filter(ImageFilter.SHARPEN)
#
#         # Enhance clarity
#         enhancer = ImageEnhance.Sharpness(image)
#         image = enhancer.enhance(clarity_factor)
#         logger.info("image processed successfully....")
#         print("image processed successfully....")
#         processed_image = np.array(image)
#         gray_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
#
#         # Configure Tesseract for more accuracy
#         # thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#         # custom_config = r'--oem 3 --psm 6'  # Adjust PSM and OEM as needed
#         # extracted_text = pytesseract.image_to_string(thresh, config=custom_config, lang='eng')
#
#
#         # Apply OCR to extract text from the scanned image
#         logger.info("Extracting Text from converted image using AI Tools...")
#         print("Extracting Text from converted image using AI Tools...")
#         extracted_text = pytesseract.image_to_string(gray_image)
#
#         Total_Extracted_Text+=f"******************************page{page_number+1}*************************************"
#         Total_Extracted_Text += "\n"
#         Total_Extracted_Text+=extracted_text
#         Total_Extracted_Text+="\n"
#
#
#         logger.info(f"Text Extracted Successfully from Page {page_number}......")
#     pdf_document.close()
        # if page_number+1 == 3:
        #     pass
    # title validation
    # if len(Total_Extracted_Text)>100:
    #     store_extracted_data = open(f"extracted_data_in_text_format\\{file_name[:-4]}.txt", "w+")
    #     store_extracted_data.write(Total_Extracted_Text)
    #     store_extracted_data.close()
    Total_Extracted_Text = open(f"extracted_data_in_text_format\\{file_name[:-4]}.txt").read()
    segragated_data = {
        "FILE_NAME":file_name,
        "TITLE":title_flag,
        "ORIGINAL_FOR_RECIPIENT":None,
        "Digital_Signature":None,
        "VEHICLE_NUMBER":None,
        "HSN_CODE":None,
        "CONSIGNEE": {"GSTN":None, "NAME":None, "STATE":None, "STATE_CODE":None},
        "CONSIGNOR": {"GSTN":None, "NAME":None, "STATE":None, "STATE_CODE":None,"PO_NUMBER":None,"INVOICE_NUMBER":None},

    }
    print("Checking Title....")
    tax_invoice_title = ["Tax Invoice","ax invoi"]

    for title_assumption in tax_invoice_title:
        if title_flag == None and title_assumption.lower() in Total_Extracted_Text.lower():
            print(f"Tax Invoice is present in Extracted Data")
            title_flag = "Available"
            segragated_data["TITLE"] = title_flag

    def gst_validation(Total_Extracted_Text):
        # possibility and data correction
        partial_pattern = r'\b[A-Z0-9]{15}\b'
        partial_gst_possibilities = re.findall(partial_pattern, Total_Extracted_Text)
        corrected_partial_possibilities = []
        for fetched_data in partial_gst_possibilities:
            corrected_pattern = ''
            corrected_pattern += fetched_data[:2].replace('O', '0')
            corrected_pattern += fetched_data[2:7].replace('0', 'O')
            corrected_pattern += fetched_data[7:11].replace('O', '0')
            corrected_pattern += fetched_data[11].replace('0', '0')
            corrected_pattern += fetched_data[12].replace('O', '0')
            corrected_pattern += fetched_data[13].replace('2', 'Z')
            corrected_pattern += fetched_data[14]

            corrected_partial_possibilities.append(corrected_pattern)

        # exact
        exact_pattern = r'\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9]{1}[A-Z]{1}[A-Z0-9]{1}\b'
        exact_pattern_gst = set(re.findall(exact_pattern, " ".join(corrected_partial_possibilities)))

        if len(exact_pattern_gst) < 2:
            for gst_number in set(corrected_partial_possibilities):
                if gst_number not in exact_pattern_gst and gst_number[-2] == 'Z':
                    exact_pattern_gst.add(gst_number)

        return list(exact_pattern_gst)


    gst_numbers = gst_validation(Total_Extracted_Text)

    def Gst_Segragation(gst_numbers):
        l_and_t_gst_file = open('l&T_GST_LIST.txt', 'r')
        l_and_t_gst_data = l_and_t_gst_file
        l_and_t_gst_gst = [line.split(',')[0] for line in l_and_t_gst_data]

        # GST Segregation
        for extracted_gst in gst_numbers:
            if extracted_gst in l_and_t_gst_gst:
                print(f"{extracted_gst} belongs to L&T Itself")
                segragated_data["CONSIGNEE"]["GSTN"] = extracted_gst

            else:
                print(f"{extracted_gst} belongs to consignor")
                segragated_data["CONSIGNOR"]["GSTN"] = extracted_gst

        return segragated_data


    segragated_data = Gst_Segragation(gst_numbers)

    def State_Segragation(segragated_data):
        State_file = open("state_codes.txt")
        State_data = State_file.readlines()
        State_Names = {state.split(',')[1]: state.split(',')[0].upper() for state in State_data}
        for state_code, state_name in State_Names.items():
            state_code = state_code[:2]
            if state_code == segragated_data["CONSIGNEE"]["GSTN"][:2]:
                segragated_data["CONSIGNEE"]["STATE"] = state_name
                segragated_data["CONSIGNEE"]["STATE_CODE"] = state_code
            if state_code == segragated_data["CONSIGNOR"]["GSTN"][:2]:
                segragated_data["CONSIGNOR"]["STATE"] = state_name
                segragated_data["CONSIGNOR"]["STATE_CODE"] = state_code

        return segragated_data

    segragated_data = State_Segragation( segragated_data)

    def PO_Number_Identifier(data,segragated_data):
        if 'OGSP' in data and '' in data:
            start_index = data.index(r'OGSP/')
            fetched_po_number = data[start_index:start_index + 25]
            segragated_data["CONSIGNOR"]["PO_NUMBER"] = fetched_po_number.split(' ')[0]


        return segragated_data

    segragated_data = PO_Number_Identifier(Total_Extracted_Text,segragated_data)


    def Inv_Num_Identifier(data,segragated_data):
        inv_indexes = []
        inv_number_flags = ["INV. NUMBER", "INV NO.", "INVOICE NUMBER", "INVOICE NO.", "INV. NO.", "INV NO", "INV",
                            "INVOICE"]
        start_index = 0
        captured_data = set()
        for inv_flag in inv_number_flags:
            if inv_flag in data.upper():
                data_to_check = data.upper()
                while True:
                    index = data_to_check.find(inv_flag, start_index)
                    if index == -1:
                        break

                    inv_indexes.append(index)
                    start_index = index + 1
        split_pattern = r'[ \n\\.,]'
        for inv_index in inv_indexes:
            if r"/" in data[inv_index:inv_index + 16 + 11]:
                inv_number_possibilities = re.split(split_pattern,data[inv_index:inv_index + len(inv_flag) + 16 + 11])
                for ele in inv_number_possibilities:
                    if r'/' in ele and len(ele) > 3:

                        captured_data.add(ele)
        if len(captured_data) == 1:
            segragated_data["CONSIGNOR"]["INVOICE_NUMBER"] = list(captured_data)[0]
        elif len(captured_data) > 1:
            segragated_data["CONSIGNOR"]["REST_DATA"] = captured_data

        return segragated_data

    segragated_data = Inv_Num_Identifier(Total_Extracted_Text, segragated_data)


    def Original_for_Rec_Validation(data, segragated_data):
        if "inal for rec" in data.lower() or "original" in data[:200].lower():
            print("*-*-*---*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*--*ORIGINAL Keyword is Availalble in data")
            segragated_data["ORIGINAL_FOR_RECIPIENT"] = "ORIGINAL Keyword is Availalble in data"
        return segragated_data

    segragated_data=Original_for_Rec_Validation(Total_Extracted_Text,segragated_data)
    print(segragated_data)


    def Digital_Sign_Validation(data, segragated_data):
        sign_keyword = ["digital signature", "digitally signed"]
        for sign in sign_keyword:
            if sign in data or sign.upper() in data.upper():
                segragated_data["Digital_Signature"] = "Digital Signature Keyword is available in document"
        return segragated_data

    segragated_data = Digital_Sign_Validation(Total_Extracted_Text, segragated_data)
    print(segragated_data)
    def Consignee_Name_Validation(data, segragated_data):
        L_and_T_Possible_names = ["L&T", "Larsen", "Toubro", "L & T"]
        for possible_name in L_and_T_Possible_names:
            if possible_name in data or possible_name.upper() in data:
                segragated_data["CONSIGNEE"]["NAME"] = possible_name
                if possible_name == "Larsen" or possible_name == "Toubro":
                    segragated_data["CONSIGNEE"]["NAME"] = "Larsen & Toubro"

        return segragated_data

    segragated_data = Consignee_Name_Validation(Total_Extracted_Text,segragated_data)

    def Truck_number_validation(data,segragated_data):
        Truck_Number_Pattern_1 = r'\b[A-Z]{2}\s\d{2}\s[A-Z]{2}\s\d{4}\b'
        # Truck_Number_Pattern_2 = r'\b[A-Z]{3}\d{3}\b'

        if "truck" in data.lower() or "vehicle" in data.lower():
            truck_pattern_1 = re.findall(Truck_Number_Pattern_1, data)
            if len(truck_pattern_1) ==1:
                segragated_data["VEHICLE_NUMBER"] = truck_pattern_1[0]
        return segragated_data

    segragated_data = Truck_number_validation(Total_Extracted_Text,segragated_data)



    # def Hsn_number_validation(data,segragated_data):
    #     pass
        # return segragated_data

    # segragated_data = Hsn_number_validation(Total_Extracted_Text, segragated_data)


    # def Consignor_Name_Validation(data, segragated_data):
    #     pass

    # print(segragated_data)
    return segragated_data



if __name__ == "__main__":
    row_number = 1
    for file_name in files:
        row_number += 1
        pdf_file = f"{folder_path}\\{file_name}"
        try:
            result = pdf_to_image_to_text(pdf_file, file_name, row_number)
        except:
            pass
        else:

            df.at[row_number-1, 'SrNo'] = row_number-1
            df.at[row_number-1, 'File_Name'] = result['FILE_NAME']
            df.at[row_number-1, 'Title'] = result['TITLE']
            df.at[row_number-1, 'PO_Number'] = result['CONSIGNOR']['PO_NUMBER']
            df.at[row_number-1,'Consignee'] = result['CONSIGNEE']['NAME']
            df.at[row_number-1, 'Consignee_GST_No'] = result['CONSIGNEE']['GSTN']
            df.at[row_number-1, 'Consignee_State_Name'] = result['CONSIGNEE']['STATE']
            df.at[row_number-1, 'Consignee_State_Code'] = result['CONSIGNEE']['STATE_CODE']
            # df.at[row_number-1,'Consignor_Name'] = result['CONSIGNOR']['NAME']
            df.at[row_number-1, 'Consignor_GST_No'] = result['CONSIGNOR']['GSTN']
            df.at[row_number-1, 'Consignor_State_Name'] = result['CONSIGNOR']['STATE']
            df.at[row_number-1, 'Consignor_State_Code'] = result['CONSIGNOR']['STATE_CODE']
            df.at[row_number-1,'Original_For_Recipient'] = result['ORIGINAL_FOR_RECIPIENT']
            df.at[row_number-1,'Tax_Invoice_Number'] = result['CONSIGNOR']['INVOICE_NUMBER']
            # df.at[row_number-1,'HSN/SAC'] =
            df.at[row_number-1,'Vehicle_Number'] = result["VEHICLE_NUMBER"]
            df.at[row_number-1,'RCM_Status'] = result['Digital_Signature']


    df.to_csv('output1.csv')
    df.drop(['SrNo', 'RCM_Status'], axis=1, inplace=True)
    df2 = df.dropna(thresh=3).reset_index()
    df2.drop("index", axis=1, inplace=True)
    df2.fillna("Not Available")
    df2.to_csv('output_final.csv')
    files_to_move_pass = df2['File_Name'].to_list()
    files_to_move_fail = [i for i in df['File_Name'].to_list() if i not in files_to_move_pass]
    for file in files_to_move_pass:
        move_file(f"sample_pdf\\{file}", "data_extraction_pass")
    for file in files_to_move_fail:
        move_file(f"sample_pdf\\{file}", "data_extraction_fail")

