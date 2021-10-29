from io import TextIOWrapper
from textUtils import *
from transformAsm import get_asm_unified, transform_asm
import os

pret_folder = os.path.join(os.sep, 'Users', 'chenghanng', 'Documents', 'PRET', 'pmd-red')

function_location = 'code_80718D8'
function_name = 'DecideUseItem'
function_header = 'void %s(struct DungeonEntity *pokemon)' % function_name
new_location = 'dungeon_ai_items'

def overwrite_file(file: TextIOWrapper, text: str):
  file.seek(0)
  file.write(text)
  file.truncate()

makefile = os.path.join(pret_folder, 'Makefile')
with open(makefile, 'r+') as file:
  contents = file.read()
  contents = contents.replace('sha1sum', 'shasum')
  overwrite_file(file, contents)

old_asm_path = os.path.join(pret_folder, 'asm', function_location + '.s')
with open(old_asm_path, 'r+') as file:
  contents = file.read()
  function_index = index_before(contents, '\tthumb_func_start ' + function_name)
  function_end_index = index_after(contents, '\tthumb_func_end %s\n' % function_name, function_index)
  function_text = contents[function_index:function_end_index]
  after_function_text = contents[function_end_index:]

  next_function_name = text_between(after_function_text, 'thumb_func_start ', '\n')
  if 'sub_' in next_function_name:
    new_asm_location = next_function_name.replace('sub_', 'code_')
  else:
    new_asm_location = 'code_' + next_function_name
    print('Next ASM function is already named. Using %s for new ASM file name.' % new_asm_location)

  contents = contents[:function_index] + '\t.align 2, 0'
  overwrite_file(file, contents)

raw_asm_file = os.path.join('asm', 'raw.txt')
with open(raw_asm_file, 'w') as file:
  file.write(function_text)

transform_asm()

new_asm_path = os.path.join(pret_folder, 'asm', new_asm_location + '.s')
with open(new_asm_path, 'w') as file:
  header = """\t.include "constants/gba_constants.inc"
\t.include "asm/macros.inc"

\t.syntax unified

\t.text
"""
  file.write(header + after_function_text)

new_location_header = os.path.join(pret_folder, 'include', new_location + '.h')
with open(new_location_header, 'w') as file:
  caps_new_location = new_location.upper()

  source = """#ifndef GUARD_%s_H
#define GUARD_%s_H

// 0x
%s;

#endif
""" % (caps_new_location, caps_new_location, function_header)
  file.write(source)

new_location_source = os.path.join(pret_folder, 'src', new_location + '.c')
with open(new_location_source, 'w') as file:
  asm_unified = get_asm_unified(function_text)
  source = """#include "global.h"
#include "%s.h"

NAKED
%s
{
    %s
}
""" % (new_location, function_header, asm_unified)
  file.write(source)

ld_script = os.path.join(pret_folder, 'ld_script.txt')
with open(ld_script, 'r+') as file:
  contents = file.read()
  contents = insert_after(contents, 'asm/%s.o(.text);\n' % function_location, '        src/%s.o(.text);\n        asm/%s.o(.text);\n' % (new_location, new_asm_location))
  overwrite_file(file, contents)
