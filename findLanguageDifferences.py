from filePaths import *
from typing import List
import os

overlay = '34'
file_name = f'pmdsky_{overlay}'
start_label_us = 'ov34_022DC958'
start_label_eu = 'ov34_022DD210'
current_line_us = None
current_line_eu = None

use_transformed = False

if use_transformed:
  with open(os.path.join('bytes', f'ov{overlay}_us.s'), 'r') as file:
    lines_us = file.readlines()
  with open(os.path.join('bytes', f'ov{overlay}_eu.s'), 'r') as file:
    lines_eu = file.readlines()
else:
  with open(os.path.join(NDSDISASM_FOLDER, 'output', f'{file_name}.s'), 'r') as file:
    lines_us = file.readlines()
  with open(os.path.join(NDSDISASM_FOLDER, 'output', 'eu', f'{file_name}.s'), 'r') as file:
    lines_eu = file.readlines()

def find_start_line(lines: List[str], start_label: str) -> int:
  if not start_label:
    return 0
  for i, line in enumerate(lines):
    if line.startswith(f'{start_label}:'):
      return i
  raise RuntimeError(f'Could not find {start_label}.')

if current_line_us is None:
  current_line_us = find_start_line(lines_us, start_label_us)
  current_line_eu = find_start_line(lines_eu, start_label_eu)

ignore_strings = [
  '_func_',
  ':',
  '@',
  '.global',
  '.word',
  '\tb ',
  '\tbeq ',
  '\tbge ',
  '\tbgt ',
  '\tbhi ',
  '\tbhs ',
  '\tbl ',
  '\tble ',
  '\tblo ',
  '\tbls ',
  '\tblt ',
  '\tblx ',
  '\tbmi ',
  '\tbne ',
  '\tbpl ',
  ]

while current_line_eu < len(lines_eu) and current_line_us < len(lines_us):
  line_eu = lines_eu[current_line_eu]
  line_us = lines_us[current_line_us]

  skip_line = False
  for ignore_string in ignore_strings:
    if ignore_string in line_eu:
      skip_line = True
      break

  if not skip_line and line_eu != line_us:
    print('Found line mismatch.')
    print(f'US ({current_line_us + 1}): {line_us}')
    print(f'EU ({current_line_eu + 1}): {line_eu}')
    break

  current_line_eu += 1
  current_line_us += 1
