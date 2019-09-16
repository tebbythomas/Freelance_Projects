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
# To compress files to .tar.gz and extract .tar.gz files
import tarfile



# Function to create a zip file
def zipdir(path, ziph):
    print("In ZIP Directory Function")
    # ziph is zipfile handle
    # Zipping all the created files
    for root, dirs, files in os.walk(path):
        for file in files:
            print("Zipping file:", os.path.join(root, file))
            ziph.write(os.path.join(root, file))


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
def extract_tar_files(fname):
    if (fname.endswith("tar.gz")):
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


def compress_zip_files(path):
    return


def extract_zip_files(path_to_zip_file, input_path):
    print("In extract zip files function!!!!!!")
    print("Path to ip file:")
    print(path_to_zip_file)
    print("Input path:")
    print(input_path)
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
    # Where input zips are located
    input_path = cwd + "/Input/"
    # Where output files will be created and later zipped
    main_output_path = cwd + "/Output/"
    for root, dirs, files in os.walk(input_path):
        for file in files:
            # Only extract zip files
            if file.endswith((".zip") or ("tar.gz") or (".gz")):
                if file.endswith((".zip")):
                    path_to_zip_file = os.path.join(root, file)
                    # So that the final output zip file has the same name as the input zip file
                    output_zip_file_name = file
                    extracted_path = extract_zip_files(path_to_zip_file, input_path)
                elif file.endswith(("tar.gz") or (".gz")):
                    extract_tar_files(file)
                    extracted_path = input_path + "Extracted"
                list_dir = os.listdir(extracted_path)
                print("First level Directories:")
                for first_level_dir in list_dir:
                    if "__MACOSX" not in first_level_dir:
                        search_path = os.path.join(extracted_path, first_level_dir)
                        output_path = extracted_path
                        output_path = output_path.replace("/Input/Extracted", "/Output/")
                        output_file_name = first_level_dir + ".txt"
                        if not os.path.exists(output_path):
                            os.makedirs(output_path)
                        output_file = open(os.path.join(output_path, output_file_name), "w")
                        # Walking through the extracted file path to read sgml files
                        for root, dirs, files in os.walk(search_path):
                            for file in files:
                                # We are only interested in .sgml files, __MACOSX is
                                # a folder created automatically after extracting the zipped files. Ignore this
                                if file.endswith((".sgml")) and "__MACOSX" not in root:
                                    print("Reading ony Japanse characters in file : ", os.path.join(root, file))
                                    input_file = open(os.path.join(root, file), "r")
                                    # Maintaining the same folder structure as the input folder
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
                                    # Closing input file handlers
                                    input_file.close()
                                    output_file.write("\n\n")
                        output_file.close()
                        fname = make_tarfile(output_file_name)
                    # Zipping up all contents of the newly created Output folder
                    # which has contents of the previously read .zip file
                    # zipf = zipfile.ZipFile(output_zip_file_name, 'w', zipfile.ZIP_DEFLATED)
                    # zipdir("Output/", zipf)
                    # Removing the created Output directory path
                    # shutil.rmtree(main_output_path)
                    # Removing the created Extracted directory path
                shutil.rmtree(extracted_path)
                    # zipf.close()


# Entry point of code
if __name__ == '__main__':
    main()
