#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

import os
import sys
import re
import csv
import shutil
from tqdm import tqdm

def main():
    'entry point'

  # CONFIGURATION
  csv_file = "xx_hashes.csv"  # Path to your CSV file
  old_root = "/mnt/c/emh/gdrive_sync"  # Root directory in original file paths
  new_root = "/mnt/c/emh/gdrive_dedup"  # New root where unique files will be copied

  # Create destination root if it doesn't exist
  os.makedirs(new_root, exist_ok=True)

  # Keep track of seen hashes
  seen_hashes = set()

  # Read all CSV lines first
  with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    rows = list(reader)

  # Initialize progress bar
  with tqdm(total=len(rows), desc="Copying unique files") as pbar:
    for file_hash, file_path in rows:
      if file_hash not in seen_hashes:
        seen_hashes.add(file_hash)

        # Compute new destination path
        if not file_path.startswith(old_root):
          print(f"Warning: Skipping {file_path}, does not start with {old_root}")
          pbar.update(1)
          continue

        relative_path = os.path.relpath(file_path, old_root)
        dest_path = os.path.join(new_root, relative_path)

        # Create parent directories as needed
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        # Copy file
        try:
          shutil.copy2(file_path, dest_path)
        except Exception as e:
          print(f"Error copying {file_path} -> {dest_path}: {e}")

      pbar.update(1)

if __name__ == '__main__':
    main()
