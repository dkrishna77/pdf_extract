import pytesseract
import cv2
import pandas as pd
from PIL import Image

# Load the image
image_path = 'page_1.png'  # Replace with the path to your image file
image = Image.open(image_path)

# Perform OCR on the image to extract text
text = pytesseract.image_to_string(image)

# Split the text into lines
lines = text.split('\n')

# Determine the table structure (you may need to customize this logic)
table_start = None
table_end = None
for i, line in enumerate(lines):
    if "Header_Column1" in line and "Header_Column2" in line:
        table_start = i + 1
    if table_start is not None and not line.strip():
        table_end = i
        break

# Extract the table data
if table_start is not None and table_end is not None:
    table_data = [line.split() for line in lines[table_start:table_end]]

    # Create a DataFrame from the table data
    df = pd.DataFrame(table_data, columns=["Header_Column1", "Header_Column2"])

    # Save the data to an Excel file
    excel_file_path = 'output_data.xlsx'
    df.to_excel(excel_file_path, index=False)

    print(f'Data has been successfully converted and saved to {excel_file_path}')
else:
    print('No table found in the')
