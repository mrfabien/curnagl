# this doesn't create a new folder if it doesn't exist, it just moves the files to the corresponding folder in the destination directory

import os
import re
import shutil

def organize_and_transfer_files(source_dir, destination_dir):
    # Check if both directories exist
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    if not os.path.exists(destination_dir):
        print(f"Destination directory '{destination_dir}' does not exist.")
        return
    
    # Get list of files in the source directory
    files = os.listdir(source_dir)
    
    # Create a dictionary to store files for each variable
    variable_files = {}
    
    # Group files by variable name
    for file in files:
        source_path = os.path.join(source_dir, file)
        # Extract variable name from the file name using regular expression
        match = re.match(r'ERA5_\d+-\d+_(.+)\.nc', file)
        if match:
            variable_name = match.group(1)
            if variable_name not in variable_files:
                variable_files[variable_name] = []
            variable_files[variable_name].append(source_path)
        else:
            print(f"Could not extract variable name from '{file}'")

    # Transfer files for each variable to the corresponding folder in the destination directory
    for variable_name, file_paths in variable_files.items():
        destination_folder = os.path.join(destination_dir, variable_name)
        # Check if the variable name folder exists
        if os.path.exists(destination_folder):
            # Move files to the variable folder
            for file_path in file_paths:
                filename = os.path.basename(file_path)
                destination_path = os.path.join(destination_folder, filename)
                shutil.move(file_path, destination_path)
                print(f"Moved '{filename}' to '{destination_folder}'")
        else:
            print(f"Folder '{variable_name}' does not exist in '{destination_dir}'. Skipping...")

# Example usage:
source_directory = "/work/FAC/FGSE/IDYST/tbeucler/default/fabien/repos/curnagl/missing_var/"
destination_directory = "/work/FAC/FGSE/IDYST/tbeucler/default/raw_data/ECMWF/ERA5/SL"
organize_and_transfer_files(source_directory, destination_directory)
