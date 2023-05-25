import os, re
from dataclasses import dataclass
from typing import List

start_address = 0x83B0000
current_address = start_address

with open(os.path.join('pointer', 'raw.txt'), 'r') as raw_file:
  raw_text = raw_file.readlines()

@dataclass
class BinLine:
  address: int
  raw_line: str
  new_line: str
  prefix_lines: List[str]

@dataclass
class ReplaceLine:
  address: int
  prefix_lines: List[str]

bin_lines = []
bin_line_memory_map = {}

def add_bin_line(line):
  global bin_lines, bin_line_memory_map
  if line[-1] != '\n':
    line += '\n'
  bin_line = BinLine(current_address, line, line, [])
  bin_lines.append(bin_line)
  bin_line_memory_map[current_address] = bin_line

current_sections = []
def add_current_part():
  global current_sections, current_address
  joined_parts = ','.join(current_sections)
  if not joined_parts.startswith('.byte'):
    joined_parts = f'.byte {joined_parts.lstrip()}'
  add_bin_line(joined_parts)
  current_address += len(current_sections)
  current_sections = []

for line in raw_text:
  bin_size = 0

  if line.startswith('.byte'):
    comma_split = line.split(',')

    for part in comma_split:
      current_sections.append(part)
      if len(current_sections) >= 4:
        add_current_part()

    if len(current_sections) > 0:
      add_current_part()

  else:
    if line.startswith('.string'):
      bin_size = len(line.split('"')[1].replace('\\0', '0'))
      address_align = current_address % 4
      if address_align > 0:
        bin_size += 4 - address_align
    elif line.startswith('.4byte'):
      bin_size = 4
    elif line.startswith('.align 2'):
      address_align = current_address % 4
      if address_align > 0:
        bin_size += 4 - address_align

    add_bin_line(line)

    if line.startswith('.global'):
      print(hex(current_address), line)

    current_address += bin_size

replace_lines = []

for line in bin_lines:
  if line.new_line.startswith('.byte'):
    match = re.search(r'(?:0x[0-f]{2}, ){3}0x08', line.new_line)
    if match:
      split_bytes = match.group(0).split(', ')
      address = ''.join(reversed(split_bytes)).replace('0x', '').upper()[1:]
      address_int = int(f'0x{address}', 16)
      if address_int <= current_address and address_int >= start_address and address_int % 4 == 0:
        pointer_name = f'gUnknown_{address}'
        replace_lines.append(ReplaceLine(address_int, [f'.global {pointer_name}\n', f'{pointer_name}:\n']))
        line.new_line = f'{line.new_line[:match.start()]}{pointer_name}{line.new_line[match.end():]}'.replace('.byte', '.4byte')

for line in replace_lines:
  if line.address in bin_line_memory_map:
    prefix_lines = bin_line_memory_map[line.address].prefix_lines
    if len(prefix_lines) == 0:
      for prefix_line in line.prefix_lines:
        prefix_lines.append(prefix_line)
  else:
    print(f'Address {hex(line.address)} not found.')

new_lines = []
for line in bin_lines:
  for prefix_line in line.prefix_lines:
    new_lines.append(prefix_line)
  new_lines.append(line.new_line)

with open(os.path.join('pointer', 'transformed.txt'), 'w') as transformed_file:
  transformed_file.writelines(new_lines)
