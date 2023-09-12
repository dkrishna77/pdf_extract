import time
time.sleep(1)
acknowledgment_message = """
*********************************************
*        Welcome to Your Program            *
*********************************************
This program is designed to process invoice PDFs
and generate an Excel file as an output.
Please ensure you have the necessary files
and resources before proceeding.
"""
# Print the acknowledgment message to the command prompt
print(acknowledgment_message)
time.sleep(5)

print("Importing Required Libraries...")


# Set the countdown start value
countdown_start = 3

# Countdown using a for loop
for i in range(countdown_start, 0, -1):
    print(f"{i}")
    time.sleep(1)