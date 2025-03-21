from dotenv import load_dotenv
import json
import random
import csv
import os
import shutil

load_dotenv()

from create_word import create_word
from test_word import test_word

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

def main():
    lan1 = "eng"
    lan2 = "es"

    restart_query = input("Do you want to restart? (y/n): ")
    if restart_query == "y":
        restart_progress() 
    
    with open("words_created.json", "r") as file2:
        words_created = json.load(file2) 
    
    with open("words_list_exp.csv", "r") as file1:
        words_list = list(csv.reader(file1))

    with open("mastery.json", "r") as file3:
        mastery = json.load(file3)

    # Start loop for creating and testing vocabulary
    while True:
        while len(mastery["mastery_0"]) < 3:
            create_word(mastery, words_list, words_created, lan1, lan2)

        # Define which mastery levels are tested with which probability
        testing_probability = [0,0,0,0,0,1,1,1,2,2,3,4,5]
        mastery_level = random.choice(testing_probability)
        if mastery[f"mastery_{mastery_level}"] != []:
            word_to_test = random.choice(mastery[f"mastery_{mastery_level}"])
            test_word(word_to_test, mastery, mastery_level, words_created, lan1, lan2)                

if __name__ == "__main__":
    main()

