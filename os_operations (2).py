import os
# Specify the directory path you want to list files from
folder_path = "sample_pdf"
# Use os.listdir() to get a list of all files and directories in the folder
files_and_directories = os.listdir(folder_path)

# Filter the list to include only files (excluding directories)
files = [f for f in files_and_directories if os.path.isfile(os.path.join(folder_path, f))]

def move_file(source_file, destination_directory):
    # Specify the destination directory where you want to move the file

    # Create the full destination file path by joining the destination directory and the file name
    destination_file = os.path.join(destination_directory, os.path.basename(source_file))

    try:
        # Use os.rename() to move the file
        os.rename(source_file, destination_file)
        print(f"File '{os.path.basename(source_file)}' moved successfully to '{destination_directory}'.")
    except FileNotFoundError:
        print("The source file does not exist.")
    except FileExistsError:
        print(f"A file with the same name already exists in '{destination_directory}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")