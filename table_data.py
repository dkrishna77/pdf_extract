#!pip install tabula-py
# from os_operations import folder_path, files
import tabula
import os
import re

def gst_validation(data):
    pattern = r'\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9]{1}[A-Z]{1}[A-Z0-9]{1}\b'
    # Find all GSTINs in the text
    gst_numbers = re.findall(pattern, data)
    return  gst_numbers

# Specify the directory path you want to list files from
folder_path = "filter1\\"
# Use os.listdir() to get a list of all files and directories in the folder
files_and_directories = os.listdir(folder_path)

# Filter the list to include only files (excluding directories)
files = [f for f in files_and_directories if os.path.isfile(os.path.join(folder_path, f))]
n =0
# Replace 'your_pdf_file.pdf' with the actual filename of your PDF.
for file in files:
    pdf_file_path = "filter1\\"+str(file)


    # Use tabula.read_pdf to extract tables and space information.
    try:
        tables = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True, lattice=True)
    except:
        tables = tabula.read_pdf(pdf_file_path, pages='all', encoding='ISO-8859-1')
    finally:
        # The 'lattice=True' option helps to extract space/layout information.
        if len(tables) != 0:
            n += 1
            print(f"****************************************{n}**{file}***************************************************")
            # Loop through the extracted tables and print the data.
            for i, table in enumerate(tables):
                print(f"Table {i + 1}:")
                # for j in table:
                # print(table)
                table_data = [row for row in table.values.tolist()]+table.columns.tolist()
                for i in table_data:

                    for j in i:
                        if len(str(j)) <=1:
                            pass
                        elif str(j) == 'nan':
                            pass
                        else:
                        # res = gst_validation(i)


                            res = gst_validation(str(j))
                            if res!= []:
                                print(res)
                            else:
                                print(j)


