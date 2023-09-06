import cv2
import pytesseract

# Load the scanned image using OpenCV
image_path = 'page_1.png'  # Replace with the path to your scanned image
image = cv2.imread(image_path)

# Convert the scanned image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply OCR to extract text from the scanned image
extracted_text = pytesseract.image_to_string(gray_image)
print(extracted_text)

# Define the HTML template
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Scanned Image to HTML</title>
</head>
<body>
    <pre>{extracted_text}</pre>
</body>
</html>
"""

# Save the HTML content to a file
html_filename = 'scanned_image2.html'
with open(html_filename, 'w', encoding='utf-8') as html_file:
    html_file.write(html_template)

print(f"HTML file '{html_filename}' has been created.")
