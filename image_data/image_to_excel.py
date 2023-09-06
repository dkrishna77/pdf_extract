import cv2
import pytesseract
import pandas as pd

# Step 1: Load the image
image_path = 'page_1.png'  # Replace with the path to your image file
image = cv2.imread(image_path)

# Step 2: Perform OCR on the image
custom_config = r'--oem 3 --psm 6'  # Tesseract OCR configuration for table extraction
extracted_text = pytesseract.image_to_string(image, config=custom_config)

# Step 3: Save the extracted text as a text file
text_file_path = 'extracted_text.txt'
with open(text_file_path, 'w') as text_file:
    text_file.write(extracted_text)

# Step 4: Read the extracted text from the text file
with open(text_file_path, 'r') as text_file:
    extracted_text = text_file.read()

# Step 5: Format and clean the extracted text as needed
# You may need to perform additional processing here to clean and structure the data.

# Step 6: Convert the text data to a DataFrame (you can customize the data structure)
# If you have tabular data, you may want to split the text into rows and columns.
# This step will depend on the specific structure of your data.

# Step 7: Save the data to an Excel file
excel_file_path = 'output_data.xlsx'
# Use pandas to create an Excel file from the structured data (e.g., DataFrame)

print(f'Data has been successfully converted and saved to {excel_file_path}')
