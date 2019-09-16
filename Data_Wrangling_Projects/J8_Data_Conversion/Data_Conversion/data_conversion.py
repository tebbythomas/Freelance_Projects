"""
Program Description:

Pre-Requisites:
There is a folder called 'Input' in the same location as this python program.
This Input folder contains the .zip and tar files which contains .sgml and .txt
files which have Japanese characters

To run the code, command is:
python data_conversion.py

Program output:
Creates a folder Output which contains 1 tar file for every compressed input file.
Each of the tar files created contain 1 compressed txt which has consolidated
Japanese content from the input files
"""

# To navigate folder structure
import os
# To perform regular expression matching
import re
# To zip and unzip files
import zipfile
# To remove intermidiary files and folders
import shutil
# To compress files to .tar.gz and extract .tar.gz files
import tarfile


# Function to create a compressed tar file
def make_tarfile(output_filename):
    # Output tar file name
    tar_name = output_filename[:-4] + ".tar.gz"
    os.chdir("Output")
    tf = tarfile.open(tar_name, mode="w:gz")
    # Adding the final .txt file containing the Japanese text as a tar file
    tf.add(output_filename)
    tf.close()
    os.remove(output_filename)
    return tar_name


# Function to extract all files within a tar file
# Reference Link: https://stackoverflow.com/questions/31163668/how-do-i-extract-a-tar-file-using-python-2-4
def extract_tar_files(fname):
    print("In Extract tar files function!")
    print("File name:")
    print(fname)
    print("Current working directory:")
    cwd = os.getcwd()
    print(cwd)
    if (fname.endswith("tar.gz") or fname.endswith(".tgz")):
        tar = tarfile.open(fname, "r:gz")
        # Extracts all the tar file contents into folder "Extracted"
        tar.extractall("Extracted")
        tar.close()
    elif (fname.endswith("tar")):
        tar = tarfile.open(fname, "r:")
        # Extracts all the tar file contents into folder "Extracted"
        tar.extractall("Extracted")
        tar.close()
    return


# Function to extract dirs and files from a zip file
# Reference Link: https://stackoverflow.com/questions/3451111/unzipping-files-in-python
def extract_zip_files(path_to_zip_file, input_path):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        # Zipped contents are extracted into a folder called /Input/Extracted
        extracted_path = input_path + "Extracted"
        # Extracts all directories and subdirectories in /Input/.zip file
        zip_ref.extractall(extracted_path)
    return extracted_path


# Main function
def main():
    # Current working directory
    cwd = os.getcwd()
    # Where input compressed files are located
    input_path = cwd + "/Input/"
    # Where output files will be created and later compressed into tar files
    main_output_path = cwd + "/Output/"
    # Navigate through complete input path
    # Reference Link: https://stackoverflow.com/questions/2922783/how-do-you-walk-through-the-directories-using-python
    for root, dirs, files in os.walk(input_path):
        for file in files:
            # Only extract zip and tar files
            if file.endswith(".zip") or file.endswith("tar.gz") or file.endswith(".gz") or file.endswith(".tgz"):
                if file.endswith(".zip"):
                    path_to_zip_file = os.path.join(root, file)
                    # Extracting contents of .zip file and storing the location
                    # of the extracted contents
                    extracted_path = extract_zip_files(path_to_zip_file, input_path)
                elif file.endswith("tar.gz") or file.endswith(".gz") or file.endswith(".tgz"):
                    # Extracting contents of the tar file
                    prev_dir = os.getcwd()
                    # Changing the current working directory
                    # Reference Link: https://stackoverflow.com/questions/431684/how-do-i-change-directory-cd-in-python
                    os.chdir(input_path)
                    extract_tar_files(file)
                    os.chdir(prev_dir)
                    # storing the location of the extracted contents
                    extracted_path = input_path + "Extracted"
                # To navigate first level directories after extracting contents
                list_dir = os.listdir(extracted_path)
                for first_level_dir in list_dir:
                    # Ignore directory __MACOSX if it is created
                    if "__MACOSX" not in first_level_dir:
                        search_path = os.path.join(extracted_path, first_level_dir)
                        output_path = extracted_path
                        # Creating the output path
                        output_path = output_path.replace("/Input/Extracted", "/Output/")
                        # Creating the output text file which will contain all Japanese content
                        output_file_name = first_level_dir + ".txt"
                        # Creating the directory structure only once
                        if not os.path.exists(output_path):
                            os.makedirs(output_path)
                        # Creating output .txt file which will later be compressed into a tar file
                        output_file = open(os.path.join(output_path, output_file_name), "w")
                        # Walking through the extracted file path to read sgml and txt files
                        for root, dirs, files in os.walk(search_path):
                            for file in files:
                                # We are only interested in .sgml files, __MACOSX is
                                # a folder created automatically after extracting the compressed files. Ignore this
                                if (file.endswith(".sgml") or file.endswith(".txt")) and "__MACOSX" not in root:
                                    print("Reading ony Japanse characters in file : ", os.path.join(root, file))
                                    input_file = open(os.path.join(root, file), "r")
                                    # Reading file line by line
                                    for line in input_file:
                                        # Reading only Japanese characters
                                        # Reference link: https://lzone.de/examples/Python%20re.sub
                                        line = re.sub('[0-9a-zA-Z<>:/]+', '', line)
                                        # Removing all leading and trailing whitespaces
                                        line = line.strip()
                                        # Do not add empty lines in the final output text file
                                        if line is not "":
                                            print(line)
                                            output_file.write(line + "\n")
                                    # Closing input file handlers
                                    input_file.close()
                                    # Writing 2 new line characters between
                                    # Japanese characters from different files
                                    output_file.write("\n\n")
                        # Closing output file handler
                        output_file.close()
                        # Compressing output txt file into a tar file
                        prev_dir = os.getcwd()
                        os.chdir(cwd)
                        fname = make_tarfile(output_file_name)
                        os.chdir(prev_dir)
                # Deleting the "Extracted" folder to save space
                # Reference Link: https://stackoverflow.com/questions/13118029/deleting-folders-in-python-recursively
                shutil.rmtree(extracted_path)


# Entry point of code
if __name__ == '__main__':
    main()
