#!pip install tabula-py

import tabula

# Replace 'your_pdf_file.pdf' with the actual filename of your PDF.
pdf_file_path = 'sample_pdf.pdf'

# Use tabula.read_pdf to extract tables and space information.
tables = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True, lattice=True)

# The 'lattice=True' option helps to extract space/layout information.

# Loop through the extracted tables and print the data.
for i, table in enumerate(tables):
    print(f"Table {i + 1}:")
    # for j in table:
    #   print(table)
    rows = table.values.tolist()
    print("Rows:")
    for row in rows:
        print(row)
    
    # Access columns
    columns = table.columns.tolist()
    print("Columns:")
    print(columns)
