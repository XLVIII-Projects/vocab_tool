import json
import os
import shutil

def restart_progress(): 
    # Define file paths
    file_to_remove = "mastery.json"  # File to delete
    source_file = "./reset/mastery.json"  # File to copy
    destination_folder = "./"  # Folder to copy into

    # Remove the existing file if it exists
    if os.path.exists(file_to_remove):
        os.remove(file_to_remove)
        print(f"Removed: {file_to_remove}")
    else:
        print("File not found, skipping deletion.")

    # Copy the new file into the destination folder
    shutil.copy(source_file, destination_folder)
    print(f"Copied {source_file} to {destination_folder}")

    with open("words_created.json", "w") as file2:
        json.dump({}, file2)