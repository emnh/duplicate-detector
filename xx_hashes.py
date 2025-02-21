#!/usr/bin/env python3

import os
import csv
import sys
import subprocess
from tqdm import tqdm

def compute_xxhash_with_cmd(file_path):
    """Use the system's xxh64sum command to compute the hash."""
    try:
        result = subprocess.run(['xxh64sum', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.split()[0]  # Extract the hash
    except Exception as e:
        print(f"Error computing hash for {file_path}: {e}")
    return None

def scan_directory(directory, output_file):
    """Recursively scan directory and compute xxHash using xxh64sum command."""
    file_list = []

    # Collect all file paths
    for root, _, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        # Show progress while processing each file
        for file_path in tqdm(file_list, desc="Computing xxHash", unit="file"):
            xx_hash = compute_xxhash_with_cmd(file_path)
            if xx_hash:
                writer.writerow([xx_hash, file_path])

if __name__ == "__main__":
    # Ensure a directory argument is provided
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory_to_scan>")
        sys.exit(1)

    directory_to_scan = sys.argv[1]

    if not os.path.isdir(directory_to_scan):
        print(f"Error: '{directory_to_scan}' is not a valid directory.")
        sys.exit(1)

    output_csv = "hashes.csv"
    scan_directory(directory_to_scan, output_csv)
    print(f"xxHash hashes written to {output_csv}")
