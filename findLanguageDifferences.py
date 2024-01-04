from filePaths import *
from typing import List
import os

overlay = 'itcm'
file_name = f'pmdsky_{overlay}'
start_label_us = None
start_label_other = None
current_line_us = None
current_line_other = None

use_transformed = False

if use_transformed:
  if overlay == 'arm9' or overlay == 'itcm':
    overlay_prefix = overlay
  else:
    overlay_prefix = f'ov{overlay}'
  with open(os.path.join('bytes', f'{overlay_prefix}_us.s'), 'r') as file:
    lines_us = file.readlines()
  with open(os.path.join('bytes', f'{overlay_prefix}_jp.s'), 'r') as file:
    lines_other = file.readlines()
else:
  with open(os.path.join(NDSDISASM_FOLDER, 'output', f'{file_name}.s'), 'r') as file:
    lines_us = file.readlines()
  with open(os.path.join(NDSDISASM_FOLDER, 'output', 'jp', f'{file_name}.s'), 'r') as file:
    lines_other = file.readlines()

def find_start_line(lines: List[str], start_label: str) -> int:
  if not start_label:
    return 0
  for i, line in enumerate(lines):
    if line.startswith(f'{start_label}:'):
      return i
  raise RuntimeError(f'Could not find {start_label}.')

if current_line_us is None:
  current_line_us = find_start_line(lines_us, start_label_us)
  current_line_other = find_start_line(lines_other, start_label_other)

ignore_strings = [
  '_func_',
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

while current_line_other < len(lines_other) and current_line_us < len(lines_us):
  line_other: str = lines_other[current_line_other]
  line_us: str = lines_us[current_line_us]
  line_other_orig = line_other
  line_us_orig = line_us

  skip_line = False
  if ':' in line_other:
    if '.4byte 0x00' not in line_other:
      skip_line = True
    else:
      line_other = line_other[line_other.find(':'):]
      line_us = line_us[line_us.find(':'):]
  else:
    for ignore_string in ignore_strings:
      if ignore_string in line_other and ignore_string in line_us:
        skip_line = True
        break


  if not skip_line and line_other != line_us:
    print('Found line mismatch.')
    print(f'US ({current_line_us + 1}): {line_us_orig}')
    print(f'JP ({current_line_other + 1}): {line_other_orig}')
    break

  current_line_other += 1
  current_line_us += 1
