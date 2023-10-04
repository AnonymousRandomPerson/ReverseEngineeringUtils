import os

from filePaths import PRET_PMDSKY_FOLDER
from typing import List

function_location = 'overlay_29_0234EC38'
function_name = 'ov29_0234FCA8'
function_header = f'u8 {function_name}()'

ASM_FOLDER = os.path.join(PRET_PMDSKY_FOLDER, 'asm')
INCLUDE_FOLDER = os.path.join(ASM_FOLDER, 'include')
HEADER_FOLDER = os.path.join(PRET_PMDSKY_FOLDER, 'include')
SRC_FOLDER = os.path.join(PRET_PMDSKY_FOLDER, 'src')
LSF_FILE_PATH = os.path.join(PRET_PMDSKY_FOLDER, 'main.lsf')

original_file_path = os.path.join(ASM_FOLDER, f'{function_location}.s')
original_inc_path = os.path.join(INCLUDE_FOLDER, f'{function_location}.inc')
with open(original_file_path, 'r') as original_file:
  original_lines = original_file.readlines()

if function_location.startswith('main'):
  file_prefix = 'main_'
else:
  file_prefix = function_location[:len('overlay_00_')]

function_start_line = None
function_end_line = None
extract_function_address = None
new_file_address = None
ADDRESS_FIND = '; 0x'
ARM_FUNC_START = '\tarm_func_start '
first_function_start_line = None

def get_line_address(line: str):
  return line[line.index(ADDRESS_FIND) + len(ADDRESS_FIND) : -1]

for i, line in enumerate(original_lines):
  if first_function_start_line is None and line.startswith(ARM_FUNC_START):
    first_function_start_line = i
  if line == f'{ARM_FUNC_START}{function_name}\n':
    function_start_line = i
  elif line.startswith(f'\tarm_func_end {function_name}'):
    function_end_line = i
  
  if function_start_line is not None and extract_function_address is None and ADDRESS_FIND in line:
    extract_function_address = get_line_address(line)
  if function_end_line is not None and ADDRESS_FIND in line:
    new_file_address = get_line_address(line)
    break

if function_start_line is None or function_end_line is None or extract_function_address is None:
  print(f'Failed to find function. Start line {function_start_line}, end line {function_end_line}, extract address {extract_function_address}, new address {new_file_address}.')
  exit(1)

remove_orig_file = first_function_start_line == function_start_line
include_new_asm_file = new_file_address is not None

new_inc_file_name = f"{file_prefix}{new_file_address}.inc"
new_asm_header = f"""\t.include "asm/macros.inc"
\t.include "{new_inc_file_name}"

\t.text
"""
new_asm_name = f'{file_prefix}{new_file_address}.s'

new_asm_lines = original_lines[function_end_line + 1:]
original_asm_lines = original_lines[:function_start_line - 1]

with open(LSF_FILE_PATH, 'r') as lsf_file:
  lsf_lines = lsf_file.readlines()

extract_file_name = f'{file_prefix}{extract_function_address}'

for i, line in enumerate(lsf_lines):
  if line.endswith(f'{function_location}.o\n'):
    if remove_orig_file:
      lsf_lines[i] = ''
    lsf_lines[i] += f'\tObject src/{extract_file_name}.o\n'
    if include_new_asm_file:
      lsf_lines[i] += f'\tObject asm/{file_prefix}{new_file_address}.o\n'
    break

BRANCH_LABEL_INSTRUCTION = '\tbl '
BRANCH_INSTRUCTION = '\tb '
WORD_KEY = '.word '
WORD_PLUS_OFFSET = ' + 0x'
def write_inc_file(lines: List[str], file_path: str):
  defined_functions = set()
  used_functions = set()
  for line in lines:
    if line.startswith(ARM_FUNC_START):
      defined_functions.add(line[len(ARM_FUNC_START) : -1])
    elif line.startswith(BRANCH_LABEL_INSTRUCTION):
      used_functions.add(line[len(BRANCH_LABEL_INSTRUCTION) : -1])
    elif line.startswith(BRANCH_INSTRUCTION):
      function = line[len(BRANCH_INSTRUCTION) : -1]
      if function[0] != '_':
        semicolon_index = function.index(' ; ')
        used_functions.add(function[:semicolon_index])
    else:
      word_index = line.find(WORD_KEY)
      if word_index >= 0 and f'{WORD_KEY}0x' not in line:
        word_plus_offset_index = line.find(WORD_PLUS_OFFSET)
        if word_plus_offset_index >= 0:
          used_functions.add(line[word_index + len(WORD_KEY) : word_plus_offset_index])
        else:
          used_functions.add(line[word_index + len(WORD_KEY) : -1])

  for function in defined_functions:
    if function in used_functions:
      used_functions.remove(function)

  write_lines = ['#pragma once\n']
  for function in sorted(used_functions):
    write_lines.append(f'.public {function}\n')

  with open(file_path, 'w') as inc_file:
    inc_file.writelines(write_lines)

if include_new_asm_file:
  with open(os.path.join(ASM_FOLDER, new_asm_name), 'w') as new_asm_file:
    new_asm_file.write(new_asm_header)
    new_asm_file.writelines(new_asm_lines)

if remove_orig_file:
  os.remove(original_file_path)
  os.remove(original_inc_path)
else:
  with open(original_file_path, 'w') as original_file:
    original_file.writelines(original_asm_lines)
  write_inc_file(original_asm_lines, original_inc_path)

if include_new_asm_file:
  write_inc_file(new_asm_lines, os.path.join(INCLUDE_FOLDER, f'{file_prefix}{new_file_address}.inc'))

with open(os.path.join(HEADER_FOLDER, f'{extract_file_name}.h'), 'w') as new_header_file:
  file_guard = f'PMDSKY_{(file_prefix + extract_function_address).upper()}_H'
  new_header_file.write(f"""#ifndef {file_guard}
#define {file_guard}

""")
  new_header_file.write(f'{function_header};\n\n')
  new_header_file.write(f'#endif //{file_guard}\n')

with open(os.path.join(SRC_FOLDER, f'{extract_file_name}.c'), 'w') as new_src_file:
  new_src_file.write(f"""#include "{extract_file_name}.h"

{function_header}
{{

}}
""")

with open(LSF_FILE_PATH, 'w') as lsf_file:
  lsf_file.writelines(lsf_lines)
