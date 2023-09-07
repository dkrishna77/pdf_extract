import openpyxl

# Load an existing Excel workbook
workbook = openpyxl.load_workbook("source.xlsx")
# Select a specific worksheet
worksheet = workbook["Sheet1"]  # Replace with the actual sheet name

