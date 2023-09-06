from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path, output_directory, output_format='jpeg', dpi=200):
    """
    Converts a PDF to a sequence of images.

    :param pdf_path: Path to the input PDF file.
    :param output_directory: Directory to save the generated images.
    :param output_format: Image format (default is 'jpeg').
    :param dpi: Dots per inch for image quality (default is 200).
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=dpi)

    # Save the images to the output directory
    for i, image in enumerate(images):
        image_path = os.path.join(output_directory, f"page_{i+1}.{output_format}")
        image.save(image_path, output_format)

if __name__ == "__main__":
    pdf_path = 'sample_pdf\\0.pdf'  # Replace with the path to your PDF file
    output_directory = '.\\'  # Replace with the directory where you want to save the images
    convert_pdf_to_images(pdf_path, output_directory)
