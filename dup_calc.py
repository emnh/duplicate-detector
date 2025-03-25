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

def main():
  'entry point'
  import csv
  import os
  from tqdm import tqdm

  # CONFIGURATION
  csv_file = "xx_hashes.csv"  # Path to your CSV file

  seen_hashes = set()
  space_saved = 0
  rows = []

  # Load all rows
  with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    rows = list(reader)

  with tqdm(total=len(rows), desc="Calculating space saved") as pbar:
    for file_hash, file_path in rows:
      if file_hash in seen_hashes:
        # This is a duplicate — add its size
        try:
          space_saved += os.path.getsize(file_path)
        except Exception as e:
          print(f"Warning: Couldn't access {file_path}: {e}")
      else:
        seen_hashes.add(file_hash)
      pbar.update(1)

  # Convert to GiB
  space_saved_gib = space_saved / (1024 ** 3)

  print(f"\nEstimated space that could be saved by removing duplicates: {space_saved_gib:.2f} GiB")

if __name__ == '__main__':
  main()
