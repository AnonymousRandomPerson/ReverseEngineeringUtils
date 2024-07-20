import os
from io import TextIOWrapper

from filePaths import PRET_PMDRED_FOLDER
from textUtils import *
from transformAsm import get_asm_unified, transform_asm

function_location = 'code_8042818'
function_name = 'sub_8042818'
function_header = f'void {function_name}(u8 a0, bool8 a1)'
new_location = 'code_804267C'
next_function_address = None

def overwrite_file(file: TextIOWrapper, text: str):
  file.seek(0)
  file.write(text)
  file.truncate()

if next_function_address:
  next_function_address = '80' + next_function_address
new_location_header = os.path.join(PRET_PMDRED_FOLDER, 'include', new_location + '.h')
existing_file = os.path.exists(new_location_header)

old_asm_path = os.path.join(PRET_PMDRED_FOLDER, 'asm', function_location + '.s')
remove_old_asm = False
with open(old_asm_path, 'r+') as file:
  contents = file.read()
  function_index = index_before(contents, '\tthumb_func_start ' + function_name)
  function_end_index = index_after(contents, f'\tthumb_func_end {function_name}\n', function_index)
  function_text = contents[function_index:function_end_index]
  after_function_text = contents[function_end_index:]

  try:
    next_function_name = text_between(after_function_text, 'thumb_func_start ', '\n')
  except AssertionError:
    print(f'No function found after {function_name}.')
    next_function_name = None

  if next_function_name:
    if 'sub_' in next_function_name:
      new_asm_location = next_function_name.replace('sub_', 'code_')
    elif next_function_address is None:
      print(f'Next ASM function is already named {next_function_name}. Enter the next address manually.')
      exit(0)
    else:
      new_asm_location = 'code_' + next_function_address
      print(f'Next ASM function is already named. Using manual function address for file name: {new_asm_location}.')
  else:
    new_asm_location = None

  contents = contents[:function_index] + '\t.align 2, 0'
  if 'thumb' in contents:
    overwrite_file(file, contents)
  else:
    os.remove(old_asm_path)
    if next_function_name is None:
      remove_old_asm = True

raw_asm_file = os.path.join('asm', 'raw.txt')
with open(raw_asm_file, 'w') as file:
  file.write(function_text)

transform_asm()

if new_asm_location:
  new_asm_path = os.path.join(PRET_PMDRED_FOLDER, 'asm', new_asm_location + '.s')
  with open(new_asm_path, 'w') as file:
    header = """\t#include "asm/constants/gba_constants.inc"
  \t#include "asm/macros.inc"

  \t.syntax unified

  \t.text
  """
    file.write(header + after_function_text)

if existing_file:
  with open(new_location_header, 'r+') as file:
    contents = file.read()
    function_header_insert =f"""{function_header};
"""
    contents = insert_before(contents, '\n#endif', function_header_insert)
    overwrite_file(file, contents)
else:
  with open(new_location_header, 'w') as file:
    caps_new_location = new_location.upper()

    source = f"""#ifndef GUARD_{caps_new_location}_H
#define GUARD_{caps_new_location}_H

{function_header};

#endif
"""
    file.write(source)

new_location_source = os.path.join(PRET_PMDRED_FOLDER, 'src', new_location + '.c')
asm_unified = get_asm_unified(function_text)
asm_unified = f"""NAKED
{function_header}
{{
    {asm_unified}
}}"""
if existing_file:
  with open(new_location_source, 'r+') as file:
    contents = file.read()
    contents = f'{contents}\n{asm_unified}\n'
    overwrite_file(file, contents)
else:
  with open(new_location_source, 'w') as file:
    source = f"""#include "global.h"
#include "{new_location}.h"

{asm_unified}
"""
    file.write(source)

ld_script = os.path.join(PRET_PMDRED_FOLDER, 'ld_script.txt')
with open(ld_script, 'r+') as file:
  contents = file.read()
  new_asm_file = f'asm/{new_asm_location}.o(.text);\n'
  anchor_file = f'asm/{function_location}.o(.text);\n'
  if remove_old_asm:
    contents = contents.replace('        ' + anchor_file, '')
  else:
    if existing_file:
      if new_asm_location:
        contents = contents.replace(anchor_file, new_asm_file)
    else:
      script_insert = (f'        src/{new_location}.o(.text);\n')
      if new_asm_location:
        script_insert = script_insert + '        ' + new_asm_file
      contents = insert_after(contents, anchor_file, script_insert)
  overwrite_file(file, contents)
