"""
Program Description:

Pre-Requisites:
There is a folder called 'Input' in the same location as this python program.
This Input folder contains the .zip file which contains .sgml files which have
Japanese characters

To run the code, command is:
python data_conversion.py

Program output:
Creates a zip file which when extracted creates a folder called Output.
All subfolders are present in the same order as the input folders. Also
the sgml files are replaced with .txt files which only contain the Japanese characters
"""

# To navigate folder structure
import os
# To perform regular expression matching
import re
# To zip and unzip files
import zipfile
# To remove intermidiary files and folders
import shutil


# Function to create a zip file
def zipdir(path, ziph):
    print("In ZIP Directory Function")
    # ziph is zipfile handle
    # Zipping all the created files
    for root, dirs, files in os.walk(path):
        for file in files:
            print("Zipping file:", os.path.join(root, file))
            ziph.write(os.path.join(root, file))


# Main function
def main():
    # Current working directory
    cwd = os.getcwd()
    # Where input zips are located
    input_path = cwd + "/Input/"
    # Where output files will be created and later zipped
    main_output_path = cwd + "/Output/"
    for root, dirs, files in os.walk(input_path):
        for file in files:
            # Only extract zip files
            if file.endswith((".zip")):
                path_to_zip_file = os.path.join(root, file)
                # So that the final output zip file has the same name as the input zip file
                output_zip_file_name = file
                with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                    # Zipped contents are extracted into a folder called /Input/Extracted
                    extracted_path = input_path + "Extracted"
                    # Extracts all directories and subdirectories in /Input/.zip file
                    zip_ref.extractall(extracted_path)
                    # Walking through the extracted file path to read sgml files
                    for root, dirs, files in os.walk(extracted_path):
                        for file in files:
                            # We are only interested in .sgml files, __MACOSX is
                            # a folder created automatically after extracting the zipped files. Ignore this
                            if file.endswith((".sgml")) and "__MACOSX" not in root:
                                print("Reading ony Japanse characters in file : ", os.path.join(root, file))
                                input_file = open(os.path.join(root, file), "r")
                                # Maintaining the same folder structure as the input folder
                                output_path = root
                                output_path = output_path.replace("/Input/Extracted/", "/Output/")
                                # Create the output folder structure only once
                                if not os.path.exists(output_path):
                                    os.makedirs(output_path)
                                # Create .txt files and not .sgml files
                                output_text_file = file[:-4] + "txt"
                                output_file = open(os.path.join(output_path, output_text_file), "w")
                                # Reading input .sgml file line by line
                                for line in input_file:
                                    # Reading only Japanese characters
                                    line = re.sub('[0-9a-zA-Z<>:/]+', '', line)
                                    # Removing all leading and trailing whitespaces
                                    line = line.strip()
                                    # Do not add empty lines in the final output text file
                                    if line is not "":
                                        print(line)
                                        output_file.write(line + "\n")
                                # Closing output and input file handlers
                                output_file.close()
                                input_file.close()
                    # Zipping up all contents of the newly created Output folder
                    # which has contents of the previously read .zip file
                    zipf = zipfile.ZipFile(output_zip_file_name, 'w', zipfile.ZIP_DEFLATED)
                    zipdir("Output/", zipf)
                    # Removing the created Output directory path
                    shutil.rmtree(main_output_path)
                    # Removing the created Extracted directory path
                    shutil.rmtree(extracted_path)
                    zipf.close()


# Entry point of code
if __name__ == '__main__':
    main()
