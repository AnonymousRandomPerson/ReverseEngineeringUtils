from io import TextIOWrapper
from filePaths import PRET_FOLDER
from textUtils import *
from transformAsm import get_asm_unified, transform_asm
import os

function_location = 'code_80521D0'
function_name = 'IsChargeMove'
function_header = 'void %s(struct DungeonEntity *pokemon, struct PokemonMove *move)' % function_name
new_location = 'charge_move'
# e.g., '80494EC'
next_function_address = None

def overwrite_file(file: TextIOWrapper, text: str):
  file.seek(0)
  file.write(text)
  file.truncate()

new_location_header = os.path.join(PRET_FOLDER, 'include', new_location + '.h')
existing_file = os.path.exists(new_location_header)

old_asm_path = os.path.join(PRET_FOLDER, 'asm', function_location + '.s')
remove_old_asm = False
with open(old_asm_path, 'r+') as file:
  contents = file.read()
  function_index = index_before(contents, '\tthumb_func_start ' + function_name)
  function_end_index = index_after(contents, '\tthumb_func_end %s\n' % function_name, function_index)
  function_text = contents[function_index:function_end_index]
  after_function_text = contents[function_end_index:]

  try:
    next_function_name = text_between(after_function_text, 'thumb_func_start ', '\n')
  except AssertionError:
    print('No function found after %s.' % function_name)
    next_function_name = None

  if next_function_name:
    if 'sub_' in next_function_name:
      new_asm_location = next_function_name.replace('sub_', 'code_')
    elif next_function_address is None:
      print('Next ASM function is already named %s. Enter the next address manually.' % next_function_name)
      exit(0)
    else:
      new_asm_location = 'code_' + next_function_address
      print('Next ASM function is already named. Using manual function address for file name: %s.' % new_asm_location)
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
  new_asm_path = os.path.join(PRET_FOLDER, 'asm', new_asm_location + '.s')
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
    function_header_insert ="""// 0x
%s;
""" % function_header
    if new_asm_location:
      search_before = '\n#endif'
    else:
      search_before = '\n// 0x'
    contents = insert_before(contents, search_before, function_header_insert)
    overwrite_file(file, contents)
else:
  with open(new_location_header, 'w') as file:
    caps_new_location = new_location.upper()

    source = """#ifndef GUARD_%s_H
#define GUARD_%s_H

// 0x
%s;

#endif
""" % (caps_new_location, caps_new_location, function_header)
    file.write(source)

new_location_source = os.path.join(PRET_FOLDER, 'src', new_location + '.c')
asm_unified = get_asm_unified(function_text)
asm_unified = """NAKED
%s
{
    %s
}""" % (function_header, asm_unified)
if existing_file:
  with open(new_location_source, 'r+') as file:
    contents = file.read()
    contents = contents + '\n' + asm_unified + '\n'
    overwrite_file(file, contents)
else:
  with open(new_location_source, 'w') as file:
    source = """#include "global.h"
#include "%s.h"

%s
""" % (new_location, asm_unified)
    file.write(source)

ld_script = os.path.join(PRET_FOLDER, 'ld_script.txt')
with open(ld_script, 'r+') as file:
  contents = file.read()
  new_asm_file = 'asm/%s.o(.text);\n' % new_asm_location
  anchor_file = 'asm/%s.o(.text);\n' % function_location
  if remove_old_asm:
    contents = contents.replace('        ' + anchor_file, '')
  else:
    if existing_file:
      if new_asm_location:
        contents = contents.replace(anchor_file, new_asm_file)
    else:
      script_insert = ('        src/%s.o(.text);\n' % new_location)
      if new_asm_location:
        script_insert = script_insert + '        ' + new_asm_file
      contents = insert_after(contents, anchor_file, script_insert)
  overwrite_file(file, contents)
