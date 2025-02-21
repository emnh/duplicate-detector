#!/usr/bin/env python3

import os
import csv
import shutil
import sys
from collections import defaultdict
from tqdm import tqdm

def find_and_move_duplicates(input_file):
    """Find duplicate hashes and move extra copies to a 'Duplicates' folder."""

    # Dictionary to store file paths by hash
    hash_dict = defaultdict(list)

    # Read CSV file
    with open(input_file, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if len(row) == 2:
                hash_dict[row[0]].append(row[1])

    # Find duplicates and prepare to move them
    duplicates_folder = os.path.join(os.path.dirname(input_file), "Duplicates")
    os.makedirs(duplicates_folder, exist_ok=True)  # Create Duplicates/ if not exist

    files_to_move = []  # List of files to move

    for files in hash_dict.values():
        if len(files) > 1:  # If more than one file has the same hash
            files_to_move.extend(files[1:])  # Keep first, move the rest

    # Move files with progress tracking
    for file_path in tqdm(files_to_move, desc="Moving duplicates", unit="file"):
        try:
            new_path = os.path.join(duplicates_folder, os.path.basename(file_path))

            # Avoid overwriting by appending a counter if needed
            counter = 1
            while os.path.exists(new_path):
                filename, ext = os.path.splitext(os.path.basename(file_path))
                new_path = os.path.join(duplicates_folder, f"{filename}_{counter}{ext}")
                counter += 1

            shutil.move(file_path, new_path)
        except Exception as e:
            print(f"Error moving {file_path}: {e}")

    print(f"Moved {len(files_to_move)} duplicate files to '{duplicates_folder}'.")

if __name__ == "__main__":
    # Ensure a CSV file argument is provided
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <hashes.csv>")
        sys.exit(1)

    hashes_file = sys.argv[1]

    if not os.path.isfile(hashes_file):
        print(f"Error: '{hashes_file}' is not a valid file.")
        sys.exit(1)

    find_and_move_duplicates(hashes_file)
