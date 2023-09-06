import pdfplumber
import pandas as pd

# Path to the image file (convert the image to PDF first)
pdf_path = 'sample_pdf\\0.pdf'

def extract_tables_from_image(pdf_path):
    tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            tables.extend(page_tables)
    
    return tables

def save_tables_to_excel(tables, excel_file):
    writer = pd.ExcelWriter(excel_file, engine='openpyxl')
    
    for i, table in enumerate(tables):
        df = pd.DataFrame(table[1:], columns=table[0])
        sheet_name = f'Table_{i + 1}'
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    writer.save()

if __name__ == "__main__":
    extracted_tables = extract_tables_from_image(pdf_path)
    
    if extracted_tables:
        excel_file_path = 'output.xlsx'
        save_tables_to_excel(extracted_tables, excel_file_path)
        print(f"Tables extracted and saved to {excel_file_path}")
    else:
        print("No tables found in the image.")
