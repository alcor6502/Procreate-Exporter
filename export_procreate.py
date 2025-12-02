
# SPDX-License-Identifier: MIT

# Procreate Recovery & Timestamp Rebuilder
# Copyright (c) 2025 Alfredo Cortellini

# Licensed under the MIT License.
# See LICENSE.md for full license text.

# Version: 2.3
# Author: Alfredo Cortellini

# Overall Description:
# This script processes folders that contain unpacked Procreate project data. It checks each subfolder in a given base directory, 
# updates or adds a timestamp-based name to the project by modifying the 'Document.archive' plist file, and then zips the folder 
# contents into a .procreate file. The timestamp is derived from the folder's creation date. The script skips invalid folders 
# and handles cases where the name is absent or already timestamped. It also preserves the original creation and modification 
# dates on the resulting .procreate file using the 'SetFile' command (macOS-specific).

# Procreate File Format:
# A .procreate file is essentially a ZIP archive that contains the project's data. Key components include:
# - 'Document.archive': A binary plist file storing metadata like the project name.
# - Other files and folders for layers, images, and additional project data.
# The script recreates this format by zipping the folder contents (excluding macOS junk like .DS_Store) and setting timestamps.

import os
import sys
import datetime
import plistlib
import zipfile
import subprocess
import shutil
import re

if shutil.which("SetFile") is None:
    print("\n WARNING: 'SetFile' is not installed on this Mac.")
    print("   Is included in the Xcode Command Line Tools.")
    print("   To install use this command:")
    print("      xcode-select --install")
    print("   Or browse:")
    print("   https://developer.apple.com/download/all/?q=command%20line%20tools\n")


def sanitize_filename(name: str, replacement: str = "_") -> str:
    """
    Convert a string into a filesystem-safe filename.
    """
    # Characters not allowed (or dangerous) on macOS/Linux/Windows
    # Includes slash, control chars, etc.
    return re.sub(r'[\/:*?"<>|\n\r\t]', replacement, name).strip()


def check_folder(dir_path: str) -> bool:
    # Checks if the given path is a valid directory containing a 'Document.archive' file.

    # Input Parameters:
    # - dir_path (str): The path to the directory to check.

    # Output:
    # - Returns True if the path is a directory and contains 'Document.archive', False otherwise.

    # Test if it is a directory
    if not (os.path.isdir(dir_path)):
        return False
    
    # Test if there is a Document.archive file
    doc_path = os.path.join(dir_path, "Document.archive")
    if not os.path.exists(doc_path):
        # print(f"  No Document.archive → skip")
        return False

    return True


def make_timestamp(dt: datetime.datetime) -> str:
    # Creates a timestamp string in the format 'YY.MM.DD-HH.mm' from a datetime object.

    # Input Parameters:
    # - dt (datetime.datetime): The datetime object to convert into a timestamp string.

    # Output:
    # - Returns a string representing the timestamp.

    AA = str(dt.year % 100).zfill(2)
    MM = str(dt.month).zfill(2)
    DD = str(dt.day).zfill(2)
    HH = str(dt.hour).zfill(2)
    mm = str(dt.minute).zfill(2)
    return f"{AA}.{MM}.{DD}-{HH}.{mm}"


def process_folder(folder_path: str, timestamp: str) -> str:
    # Processes the 'Document.archive' plist file in the folder to update or add a project name with a timestamp.
    # Handles cases where the name is absent, already timestamped, or needs updating.

    # Input Parameters:
    # - folder_path (str): The path to the folder containing 'Document.archive'.
    # - timestamp (str): The timestamp string to prepend or use as the name.

    # Output:
    # - Returns the new or existing project name as a string. Returns empty string if processing fails.

    new_name = ""

    # Read the binary plist with plistlib
    doc_path = os.path.join(folder_path, "Document.archive")
    with open(doc_path, "rb") as f:
        plist = plistlib.load(f)

    objects = plist["$objects"]
    root = objects[1]

    name_uid = root.get("name")
    if not isinstance(name_uid, plistlib.UID):
        print("************************************************************************")
        print("************* 'name' is not a UID → unexpected format, skip ************")
        print("************************************************************************")
        return new_name


    if name_uid.data == 0:
        # Name absent → create a new string object with only the timestamp
        new_name = timestamp
        print(f"  Name absent → create '{new_name}'\n")

        objects.append(new_name)
        new_uid_index = len(objects) - 1
        root["name"] = plistlib.UID(new_uid_index)

        # Rewrite the binary plist (same bplist00 format)
        with open(doc_path, "wb") as f:
            plistlib.dump(plist, f, fmt=plistlib.FMT_BINARY)
        
        return new_name

    # Name is present and strip spaces in front and at the end

    old_name = objects[name_uid.data].strip()

    if not isinstance(old_name, str):
        print("************* The existing name is not a string → Force the type *************")
        old_name = ""
    
    # Check if there is already a time stamp and do nothing
    if len(old_name) >= 14:
        if old_name[2] == '.' and old_name[5] == '.' and old_name[8] == '-' and old_name[11] == '.':
            print(f"  File name: '{old_name}'\n")
            return old_name
    
    # Check if the oldname is an empty string
    if len(old_name) == 0:
        new_name = f"{timestamp}"
    else:
        new_name = f"{timestamp} {old_name}"
    
    print(f"  Update name: '{old_name}' → '{new_name}'\n")
    objects[name_uid.data] = new_name

    # Rewrite the binary plist (same bplist00 format)
    with open(doc_path, "wb") as f:
        plistlib.dump(plist, f, fmt=plistlib.FMT_BINARY)

    return new_name


def make_procreate_file(dir_path: str, name_file: str, create_date: datetime.datetime, mod_date: datetime.datetime) -> None:
    # Creates a .procreate file by zipping the contents of the directory and sets the file's creation and modification dates.

    # Input Parameters:
    # - dir_path (str): The path to the directory to zip.
    # - name_file (str): The base name for the output .procreate file.
    # - date_file (datetime.datetime): The datetime to set as creation and modification time.

    # Output:
    # - None (creates the file on disk).
    
    # Sanitize Filename
    safe_name = sanitize_filename(name_file)

    if safe_name != name_file:
        print(f"  Sanitized filename:\n    '{name_file}'\n → '{safe_name}'")

    output_file = os.path.join(os.path.dirname(dir_path), f"{safe_name}.procreate")

    # Create the zip (.procreate is a zip)
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file == ".DS_Store":
                    continue  # exclude macOS trash
                full_path_zip = os.path.join(root, file)

                # relative path inside the archive
                rel_path_zip = os.path.relpath(full_path_zip, dir_path)

                z.write(full_path_zip, rel_path_zip)

    # Associate the original timestamp of the folder to the .procreate file

    # Format the date for SetFile (MM/DD/YYYY HH:MM:SS)
    create_date_str = create_date.strftime("%m/%d/%Y %H:%M:%S")
    mod_date_str = mod_date.strftime("%m/%d/%Y %H:%M:%S")

    # Change creation date (-d) and modification date (-m) with SetFile
    subprocess.run(["SetFile", "-d", create_date_str, output_file], check=False)
    subprocess.run(["SetFile", "-m", mod_date_str, output_file], check=False)

    return


def main():
    # Main function to process sub-folders in the base directory provided as a command-line argument.
    # For each valid subfolder, updates the name with timestamp and creates a .procreate file.

    # Input Parameters:
    # - None (uses sys.argv for base directory).

    # Output:
    # - None (processes folders and prints status).

    if len(sys.argv) < 2:
        print("Usage: python3 create_timestamp_name.py <main_folder>")
        return

    base_dir = sys.argv[1]
    print("Main folder:", base_dir)

    # Process only the first level of directories
    for entry in os.listdir(base_dir):
        full_path = os.path.join(base_dir, entry)

        if not check_folder(full_path):
            continue

        print(f"\nProcess folder: {entry}")

        # Creation date from the folder creation date
        stat_full_path = os.stat(full_path)
        creation_date = datetime.datetime.fromtimestamp(os.stat(full_path).st_birthtime)
        
        # Modification date from Document.archive modification date
        doc_path = os.path.join(full_path, "QuickLook", "Thumbnail.png")
        stat_doc_path = os.stat(doc_path)
        modification_date = datetime.datetime.fromtimestamp(stat_doc_path.st_mtime)

        # Update name of the file with a time stamp
        procreate_name = process_folder(full_path, make_timestamp(creation_date))
        
        # Check if the name has been updated correctly otherwise skip .procreate file creation
        if not procreate_name:
            continue

        # Transform the folder in a procreate file
        make_procreate_file(full_path, procreate_name, creation_date, modification_date)
            
    print("\nFinished.")

if __name__ == "__main__":
    main()
