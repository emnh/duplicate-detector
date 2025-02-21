#!/usr/bin/env python3

import os
import hashlib
import csv
from tqdm import tqdm

def compute_md5(file_path):
    """Compute MD5 hash of a file with progress bar."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            total_size = os.path.getsize(file_path)
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(file_path), leave=False) as pbar:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
                    pbar.update(len(chunk))  # Update progress bar
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error computing hash for {file_path}: {e}")
        return None

def scan_directory(directory, output_file):
    """Recursively scan directory, compute MD5 hashes, and write to CSV."""
    file_list = []

    # Collect all file paths
    for root, _, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        
        # Show progress while processing each file
        for file_path in tqdm(file_list, desc="Computing MD5 Hashes", unit="file"):
            md5_hash = compute_md5(file_path)
            if md5_hash:
                writer.writerow([md5_hash, file_path])

if __name__ == "__main__":
    directory_to_scan = input("Enter the directory to scan: ").strip()
    output_csv = "hashes.csv"
    scan_directory(directory_to_scan, output_csv)
    print(f"MD5 hashes written to {output_csv}")

