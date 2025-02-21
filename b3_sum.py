#!/usr/bin/env python3

import os
import sys
import csv
import subprocess
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def compute_b3sum(file_path):
    """Compute b3sum using the system's b3sum command in a subprocess."""
    try:
        result = subprocess.run(['b3sum', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.split()[0], file_path  # Extract hash and return as tuple
    except Exception as e:
        print(f"Error computing hash for {file_path}: {e}")
    return None

def scan_directory(directory, output_file):
    """Recursively scan directory and compute b3sum using multiprocessing."""
    file_list = [os.path.join(root, f) for root, _, files in os.walk(directory) for f in files]

    #num_workers = cpu_count()  # Get number of CPU cores
    num_workers = 1
    print(f"Using {num_workers} parallel workers...")

    with Pool(num_workers) as pool:
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            # Use tqdm for progress bar while processing files in parallel
            for result in tqdm(pool.imap_unordered(compute_b3sum, file_list), total=len(file_list), desc="Computing b3sum"):
                if result:
                    writer.writerow(result)

if __name__ == "__main__":
    # Ensure a directory argument is provided
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory_to_scan>")
        sys.exit(1)

    directory_to_scan = sys.argv[1]

    if not os.path.isdir(directory_to_scan):
        print(f"Error: '{directory_to_scan}' is not a valid directory.")
        sys.exit(1)

    output_csv = "b3_hashes.csv"
    scan_directory(directory_to_scan, output_csv)
    print(f"b3sum hashes written to {output_csv}")
