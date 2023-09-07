import cv2
import pytesseract

def check_text_in_first_half(image_path, title_to_check):
    # Load the image using OpenCV
    image = image_path

    # Get the dimensions of the image
    height, width, _ = image.shape

    # Crop the first half of the image
    cropped_image = image[:height // 2, :]

    # Convert the cropped image to grayscale
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Apply OCR to extract text from the image using Tesseract
    extracted_text = pytesseract.image_to_string(gray_image)

    # Check if the desired text is present in the extracted text
    if title_to_check in extracted_text:
        return f"The title '{title_to_check}' is present in the first half of the image."
    else:
        return f"The title '{title_to_check}' is not present in the first half of the image."