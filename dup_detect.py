#!/usr/bin/env python3

import csv
from collections import defaultdict

def find_duplicates(input_file):
    """Read CSV file and find duplicate MD5 hashes."""
    hash_dict = defaultdict(list)

    # Read CSV file
    with open(input_file, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if len(row) == 2:
                hash_dict[row[0]].append(row[1])

    # Find and print duplicates
    duplicates_found = False
    for md5sum, files in hash_dict.items():
        if len(files) > 1:
            duplicates_found = True
            print(f"\nDuplicate MD5: {md5sum}")
            for file in files:
                print(f" - {file}")

    if not duplicates_found:
        print("No duplicate files found.")

if __name__ == "__main__":
    input_csv = "xx_hashes.csv"
    find_duplicates(input_csv)
