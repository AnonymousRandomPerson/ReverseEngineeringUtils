import os
import re
from textUtils import *

def transform_asm():
  raw_file = os.path.join('asm', 'raw.txt')
  with open(raw_file, 'r') as file:
    raw_asm = file.read()

  replaced_asm = raw_asm.replace(',l', ', l').replace(',r', ', r').replace('.4byte', '.word')
  transformed_asm = ''
  for line in replaced_asm.split('\n')[2:-2]:
    match = re.search(', \d+$', line)
    if match:
      number_start = match.start() + 2
      number = int(line[number_start : match.end()])
      if number == 0 and 'mov' not in line:
        number = str(number)
      else:
        number = hex(number)
      line = line[:number_start] + '#' + number
    else:
      match = re.search(', 0x[\dABCDEF]+]?$', line)
      if match:
        number_start = match.start() + 2
        number = line[number_start : match.end()]
        line = line[:number_start] + '#' + number.lower()
    transformed_asm += line + '\n'

  transformed_file = os.path.join('asm', 'transformed.txt')
  with open(transformed_file, 'w') as file:
    file.write(transformed_asm)

def get_asm_unified(raw_asm=None):
  if raw_asm is None:
    raw_file = os.path.join('asm', 'raw.txt')
    with open(raw_file, 'r') as file:
      raw_asm = file.read()
  function_name = text_between(raw_asm, 'thumb_func_start ', '\n')
  asm_unified = text_between(raw_asm, function_name + ':\n', '\n\tthumb_func_end')
  asm_unified = '"' + asm_unified.replace('\t', '').replace('\n', '\\n"\n"') + '"'
  return 'asm_unified(%s);' % asm_unified
