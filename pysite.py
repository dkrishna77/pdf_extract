from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    # if len(text) != 0:
    return text
    # Path to the PDF file you want to extract text from

    #     print(f"data crerated for {file}")
    #     word_document = Document()
    #     word_document.add_paragraph(extracted_text)
    #     word_file = f'pysite_data\\output{file.split(".")[0]}.docx'  # Replace with your desired Word file path
    #     word_document.save(word_file)
    # else:
    #     print(f"{file} has no text data found")




