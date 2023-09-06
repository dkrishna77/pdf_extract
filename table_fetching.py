import  tabula
import re
from update_excel_sheet import worksheet, workbook

def gst_validation(data):
    pattern = r'\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9]{1}[A-Z]{1}[A-Z0-9]{1}\b'
    # Find all GSTINs in the text
    gst_numbers = re.findall(pattern, data)
    return  gst_numbers
def fetch_table_data(pdf_file_path):
    try:
        tables = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True, lattice=True)
    except:
        tables = tabula.read_pdf(pdf_file_path, pages='all', encoding='ISO-8859-1')
    finally:
        # The 'lattice=True' option helps to extract space/layout information.
        if len(tables) != 0:
            print(f"******************************************{pdf_file_path}***************************************************")
            # Loop through the extracted tables and print the data.
            for i, table in enumerate(tables):
                print(f"Table {i + 1}:")
                # for j in table:
                # print(table)
                table_data = [row for row in table.values.tolist()] + table.columns.tolist()
                for i in table_data:

                    for j in i:
                        if len(str(j)) <= 1:
                            pass
                        elif str(j) == 'nan':
                            pass
                        else:
                            # res = gst_validation(i)

                            res = gst_validation(str(j))
                            if res != []:
                                print(res)
                                # worksheet[T"{row_number}"] = file
                                # worksheet[f"S{row_number}"] = ",\n".join([i for i in (set(gst_number))])
                                # workbook.save("source.xlsx")
                            else:
                                print(j)
