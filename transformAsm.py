import os
import re
from textUtils import *

def transform_asm():
  raw_file = os.path.join('asm', 'raw.txt')
  with open(raw_file, 'r') as file:
    raw_asm = file.read()

  replaced_asm = raw_asm.replace(',l', ', l').replace(',r', ', r').replace('.4byte', '.word').replace('r10', 'sl').replace('r12', 'ip')
  transformed_asm = ''
  transformed_asm_decompme = ''
  for line in replaced_asm.split('\n')[2:-2]:
    if '.align' not in line:
      decimal_match: re.Match = re.search(r', \d+$', line)
      if decimal_match:
        number_start = decimal_match.start() + 2
        number = int(line[number_start : decimal_match.end()])
        if number == 0 and 'mov' not in line:
          number = str(number)
        else:
          number = hex(number)
        line = line[:number_start] + '#' + number
      else:
        hex_match: re.Match = re.search(r', 0x[\dABCDEF]+]?$', line)
        if hex_match:
          number_start = hex_match.start() + 2
          number = line[number_start : hex_match.end()]
          line = line[:number_start] + '#' + number.lower()
    transformed_asm += line + '\n'

    line_decompme = line
    if 'bls' not in line and 'bcs' not in line:
      line_decompme = re.sub(r'^(\t\w+)s ', r'\1 ', line)
    if not re.search(r'pop \{r[01]\}', line_decompme) and not re.search(r'bx r[01]', line_decompme):
      transformed_asm_decompme += line_decompme + '\n'

  pop_index = transformed_asm_decompme.rfind('pop')
  if pop_index >= 0:
    last_pop_end = transformed_asm_decompme.find('}', transformed_asm_decompme.rfind('pop'))
    transformed_asm_decompme = transformed_asm_decompme[:last_pop_end] + ', pc' + transformed_asm_decompme[last_pop_end:]
  else:
    has_word_end = False
    has_word = True
    line_start = len(transformed_asm_decompme)
    while (has_word):
      prev_line_start = line_start
      line_start = transformed_asm_decompme.rfind('\n', 0, line_start - 1)
      has_word = '.word' in transformed_asm_decompme[line_start:prev_line_start]
      if has_word:
        has_word_end = True
    pop_instruction = '  pop {pc}'
    if has_word_end:
      pop_instruction = '\n' + pop_instruction
    transformed_asm_decompme = transformed_asm_decompme[:prev_line_start] + pop_instruction + transformed_asm_decompme[prev_line_start:]

  transformed_file = os.path.join('asm', 'transformed.txt')
  with open(transformed_file, 'w') as file:
    file.write(transformed_asm)

  transformed_file_decompme = os.path.join('asm', 'transformed_decompme.txt')
  with open(transformed_file_decompme, 'w') as file:
    file.write(transformed_asm_decompme)

def get_asm_unified(raw_asm=None):
  if raw_asm is None:
    raw_file = os.path.join('asm', 'raw.txt')
    with open(raw_file, 'r') as file:
      raw_asm = file.read()
  function_name = text_between(raw_asm, 'thumb_func_start ', '\n')
  asm_unified = text_between(raw_asm, function_name + ':\n', '\n\tthumb_func_end')
  asm_unified = f'"{asm_unified.replace('\t', '').replace('\n', '\\n"\n"')}"'
  return f'asm_unified({asm_unified});'
