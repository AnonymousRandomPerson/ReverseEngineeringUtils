from filePaths import *
import os

file_path = os.path.join(PRET_PMDSKY_FOLDER, 'sub', 'asm', 'main.s')
file_path = 'output.txt'

old_address = 0x0200F4A8
new_address = 0x038072C0

address_shift = new_address - old_address

new_lines = []

with open(file_path, 'r') as asm_file:
  for line in asm_file.readlines():
    underscore_index = line.find('_0')
    if underscore_index >= 0:
      line_address_string = line[underscore_index + 1 : underscore_index + 9]
      line_address = int(line_address_string, 16)
      new_line_address = line_address + address_shift
      line = line.replace(line_address_string, '0' + hex(new_line_address)[2:].upper())
    new_lines.append(line)

with open(file_path, 'w') as asm_file:
  asm_file.writelines(new_lines)
