import fitz  # PyMuPDF
import nltk
nltk.download()
from nltk.corpus import brown
brown.words()
import re

nltk.download('punkt')  # Download NLTK's Punkt tokenizer data

from nltk.tokenize import word_tokenize, sent_tokenize

def extract_text_from_pdf(pdf_file):
    pdf_text = ""

    # Open the PDF file
    pdf_document = fitz.open(pdf_file)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text()
        pdf_text += text

    # Close the PDF document
    pdf_document.close()

    return pdf_text

def extract_invoice_data(text):
    invoice_data = {}

    # Define regular expressions for different data fields
    invoice_number_pattern = r'Invoice\s*Number:\s*(\d+)'
    invoice_date_pattern = r'Invoice\s*Date:\s*(\d{2}/\d{2}/\d{4})'
    total_amount_pattern = r'Total\s*Amount:\s*\$([\d,.]+)'

    # Extract data using regular expressions
    invoice_number = re.search(invoice_number_pattern, text, re.IGNORECASE)
    invoice_date = re.search(invoice_date_pattern, text, re.IGNORECASE)
    total_amount = re.search(total_amount_pattern, text, re.IGNORECASE)

    # Check if any of the data fields were found
    if invoice_number:
        invoice_data["Invoice Number"] = invoice_number.group(1)
    if invoice_date:
        invoice_data["Invoice Date"] = invoice_date.group(1)
    if total_amount:
        invoice_data["Total Amount"] = total_amount.group(1)

    return invoice_data

def main(pdf_file):
    pdf_text = extract_text_from_pdf(pdf_file)
    invoice_data = extract_invoice_data(pdf_text)

    if invoice_data:
        print("Invoice Data:")
        for key, value in invoice_data.items():
            print(f"{key}: {value}")
    else:
        print("Invoice data not found in the PDF.")

if __name__ == "__main__":
    pdf_file = "sample_pdf.pdf"  # Replace with the path to your PDF invoice
    main(pdf_file)
# !pip install PyPDF2
from PyPDF2 import PdfReader
nltk.download('stopwords')
# Replace 'your_pdf_file.pdf' with the actual filename of your PDF.
pdf_file_path = 'sample_pdf.pdf'

def extract_text_from_pdf(pdf_path):
    text = ''
    pdf_reader = PdfReader(pdf_path)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

pdf_text = extract_text_from_pdf(pdf_file_path)
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Tokenize the text into words
words = word_tokenize(pdf_text)

# Remove stopwords
stop_words = set(stopwords.words('english'))
filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

# Print the first 10 words as an example
print(words)



