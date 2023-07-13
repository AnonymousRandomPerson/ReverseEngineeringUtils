import os, re
from dataclasses import dataclass
from typing import Dict, List, Any

start_address = 0x811601C
current_address = start_address
include_unaligned_pointers = False
min_address = start_address
trailing_spaces = ''
search_4byte_addresses = False

asm_end = 0x80B6904

custom_pointers = set([
])

include_sizes = {
  'item/item_descriptions.s': 0x66A8,
  'item/item_data.inc': 0x1E00,
  'item/item_names.s': 0xC44,
  'monster/monster_data.inc': 0x7740,
  'monster/monster_names.s': 0x191C,
  'monster/learnset/learnset_data.inc': 0x6D18,
  'move/move_data.inc': 0x3A14,
  'move/move_names.s': 0x7244,
  'monster/learnset/learnset_ptrs.s': 0xD20,
  'text/save.inc': 0x35C,
}

macro_sizes = {
}
default_macro_size = 16

string_macros = {
  '{APOSTROPHE}': '~27',
  '{ARG_MOVE_ITEM_0}': '$i0',
  '{ARG_MOVE_ITEM_1}': '$i1',
  '{ARG_POKEMON_0}': '$m0',
  '{ARG_POKEMON_1}': '$m1',
  '{ARG_POKEMON_2}': '$m2',
  '{ARG_POKEMON_3}': '$m3',
  '{B_BUTTON}': 'BB',
  '{CENTER_ALIGN}': '#+',
  '{COLOR_1 ': '#C',
  '{COLOR_1}': '#C',
  '{COLOR_2 ': '#c',
  '{COLOR_2}': '#c',
  '{COMMA}': '~2c',
  'CYAN}': '5',
  'CYAN_2}': '5',
  '{END_COLOR_TEXT_1}': '#R',
  '{END_COLOR_TEXT_2}': '#r',
  '{EXTRA_MSG}': '#P',
  'GENDER_COLOR}': 'E',
  'GREEN}': '4',
  'GREEN_2}': 'I',
  'LIGHT_BLUE}': 'G',
  '{POKE}': 'POKE',
  'RED}': '2',
  'RED_2}': 'W',
  '{STAR_BULLET}': '**',
  'YELLOW}': '6',
  'YELLOW_2}': '6',
  'YELLOW_3}': 'C',
  'YELLOW_4}': 'D',
  'YELLOW_5}': 'N',
  '{WAIT_PRESS}': '#W',
  'な': 'AA',
  'し': 'AA',
}

@dataclass
class TargetRange:
  start: int
  end: int

target_pointer_ranges = [
]

print('Start address:', hex(start_address))

with open(os.path.join('pointer', 'raw.txt'), 'r') as raw_file:
  raw_text = raw_file.readlines()

@dataclass
class BinLine:
  address: int
  raw_line: str
  new_line: str
  prefix_lines: List[str]
  changed: bool
  group: Any

@dataclass
class BinLineGroup:
  raw_line: str
  bin_lines: List[BinLine]

@dataclass
class ReplaceLine:
  address: int
  prefix_lines: List[str]

bin_line_groups: List[BinLineGroup] = []
bin_lines: List[BinLine] = []
bin_line_memory_map: Dict[int, BinLine] = {}

def add_bin_line(line):
  global bin_lines, bin_line_memory_map, current_bin_line_group
  if line[-1] != '\n':
    line += '\n'
  bin_line = BinLine(current_address, line, line, [], False, current_bin_line_group)
  bin_lines.append(bin_line)
  for i in range(0, 4):
    bin_line_memory_map[current_address + i] = bin_line
  current_bin_line_group.bin_lines.append(bin_line)

current_sections = []
def add_current_part():
  global current_sections, current_address
  joined_parts = ','.join(current_sections)
  if not joined_parts.lstrip().startswith('.byte'):
    joined_parts = f'{trailing_spaces}.byte {joined_parts.lstrip()}'
  add_bin_line(joined_parts)
  current_address += len(current_sections)
  current_sections = []

unknown_macros = set()
for line in raw_text:
  line_strip = line.lstrip()
  bin_size = 0
  current_bin_line_group = BinLineGroup(line, [])
  bin_line_groups.append(current_bin_line_group)

  if line == 'gUnknown_80F67DC: @ 80F67DC' + '\n':
    print(hex(current_address))

  if line_strip.startswith('.byte'):
    comma_split = line_strip.split(',')

    for part in comma_split:
      current_sections.append(part)
      if len(current_sections) >= 4:
        add_current_part()
        current_sections = []

    if len(current_sections) > 0:
      add_current_part()

  else:
    if line_strip.startswith('.string') or line_strip.startswith('.asciz'):
      if '{' in line_strip:
        for macro, replace in string_macros.items():
          line_strip = line_strip.replace(macro, replace)
      if '{' in line_strip or '}' in line_strip:
        print('Found unknown string macro in line:', line_strip[:-1])
      
      bin_size = len(line_strip.split('"')[1].replace('\\0', '0').replace('\\n', 'n'))
    elif line_strip.startswith('.2byte'):
      bin_size = 2
    elif line_strip.startswith('.4byte'):
      bin_size = 4
    elif line_strip.startswith('.align 2'):
      address_align = current_address % 4
      if address_align > 0:
        bin_size = 4 - address_align
    elif line_strip.startswith('.incbin'):
      offset_index = line_strip.rfind(', 0x')
      if offset_index == -1:
        bin_size = 0x100
      else:
        bin_size = int(line_strip[offset_index + 2 : -1], 16)
    elif line_strip.startswith('#include'):
      include_file = line_strip[len('#include "') : -2]
      if include_file in include_sizes:
        bin_size += include_sizes[include_file]
      else:
        print('Found unknown #include:', include_file)
    elif len(line_strip):
      first = line_strip[0]
      if first != '.' and first != '@' and first != '#' and ':' not in line_strip:
        space_index = line_strip.find(' ')
        macro = line_strip[:space_index]
        if macro in macro_sizes:
          bin_size = macro_sizes[macro]
        else:
          bin_size = default_macro_size
          unknown_macros.add(macro)

    add_bin_line(line)

    current_address += bin_size

print('End address:', hex(current_address))
print('Size:', hex(current_address - start_address))

if not default_macro_size:
  for macro in sorted(unknown_macros):
    print('Found unknown macro', macro)

replace_lines = []

used_ranges = set()
for line in bin_lines:
  if len(target_pointer_ranges) > 0:
    in_target_range = False
    for target_pointer_range in target_pointer_ranges:
      if line.address >= target_pointer_range.start and line.address <= target_pointer_range.end:
        in_target_range = True
        used_ranges.add(target_pointer_range.start)
        break
    in_target_range = False
    if not in_target_range:
      continue
  
  new_line_strip = line.new_line.lstrip()
  replace_line = None
  if new_line_strip.startswith('.byte'):
    match = re.search(r'(?:0x[0-f]{2}, ){3}0x0[89]', new_line_strip)
    if match:
      split_bytes = match.group(0).split(', ')
      address = ''.join(reversed(split_bytes)).replace('0x', '').upper()[1:]
      replace_line = lambda pointer_name : f'{new_line_strip[:match.start()]}{pointer_name}{new_line_strip[match.end():]}'.replace('.byte', '.4byte')
  elif search_4byte_addresses:
    match = re.search(r'0x(82[0-F]{5})\n', new_line_strip)
    if match:
      address = match.group(1)
      replace_line = lambda pointer_name : new_line_strip.replace('0x82', 'gUnknown_82')

  if replace_line:
    address_int = int(f'0x{address}', 16)

    address_alignment = address_int % 4
    if include_unaligned_pointers or address_alignment <= 1:
      in_data_range = address_int <= current_address and address_int >= min_address
      potential_data_pointer = in_data_range and address_alignment == 0
      potential_function_pointer = address_int < asm_end and address_alignment == 1
      if potential_data_pointer or address_int in custom_pointers:
        pointer_name = f'gUnknown_{address}'
        replace_lines.append(ReplaceLine(address_int, [f'.global {pointer_name}\n', f'{pointer_name}:\n']))
        line.new_line = trailing_spaces + replace_line(pointer_name)
        line.changed = True
      elif potential_function_pointer:
        print(f'Found possible function pointer at address {hex(line.address)}: {hex(address_int)}')
        pointer_name = f'sub_{hex(address_int - 1).upper()}'.replace('0X', '')
        line.new_line = trailing_spaces + replace_line(pointer_name)
        line.changed = True
      elif address_alignment == 0 and not in_data_range:
        print(f'Found possible pointer outside range at address {hex(line.address)}: {hex(address_int)}')

for pointer in custom_pointers:
  pointer_name = f'gUnknown_{hex(pointer)[2:].upper()}'
  replace_lines.append(ReplaceLine(pointer, [f'.global {pointer_name}\n', f'{pointer_name}:\n']))

# for range in used_ranges:
#   print(hex(range))
print(f'Found {len(replace_lines)} pointers.')
missing_addresses = set()

for line in replace_lines:
  if line.address in bin_line_memory_map:
    #print(hex(line.address))
    pointer_line = bin_line_memory_map[line.address]
    if line.address != pointer_line.address:
      comma_split = pointer_line.new_line[6:-1].split(', ')
      insert_index_whole = bin_lines.index(pointer_line)
      insert_index_group = pointer_line.group.bin_lines.index(pointer_line)
      old_address = pointer_line.address
      del bin_lines[insert_index_whole]
      del pointer_line.group.bin_lines[insert_index_group]
      for i, byte in enumerate(comma_split):
        byte_line = f'{trailing_spaces}.byte {byte}\n'
        new_address = old_address + i
        new_line = BinLine(new_address, byte_line, byte_line, [], False, pointer_line.group)
        if new_address == line.address:
          pointer_line = new_line
        bin_lines.insert(insert_index_whole + i, new_line)
        pointer_line.group.bin_lines.insert(insert_index_group + i, new_line)
        bin_line_memory_map[new_address] = new_line
    
    pointer_line.changed = True
    prefix_lines = pointer_line.prefix_lines
    if len(prefix_lines) == 0:
      for prefix_line in line.prefix_lines:
        prefix_lines.append(trailing_spaces + prefix_line)
  else:
    missing_addresses.add(line.address)

for address in sorted(missing_addresses):
  print(f'Address {hex(address)} not found.')

new_lines = []

def combine_byte_string(current_byte_string: str):
  return f'{trailing_spaces}.byte {", ".join(current_byte_string)}\n' 

for group in bin_line_groups:
  changed = any([bin_line.changed for bin_line in group.bin_lines])
  if changed:
    group_line_strip = group.raw_line.lstrip()
    if group_line_strip.startswith('.byte'):
      current_byte_string: List[str] = []

      for line in group.bin_lines:
        line_strip = line.new_line.lstrip()
        if line_strip.startswith('.4byte'):
          if len(current_byte_string) > 0:
            new_lines.append(combine_byte_string(current_byte_string))
            current_byte_string = []
          for prefix_line in line.prefix_lines:
            new_lines.append(prefix_line)
          new_lines.append(line.new_line)
        elif line_strip.startswith('.byte'):
          if len(line.prefix_lines) > 0 and len(current_byte_string) > 0:
            new_lines.append(combine_byte_string(current_byte_string))
            current_byte_string = []
          for prefix_line in line.prefix_lines:
            new_lines.append(prefix_line)
          current_byte_string.append(line_strip[6:-1])
        else: 
          for prefix_line in line.prefix_lines:
            new_lines.append(prefix_line)

      if len(current_byte_string) > 0:
        new_lines.append(combine_byte_string(current_byte_string))

    else:
      for line in group.bin_lines:
        for prefix_line in line.prefix_lines:
          new_lines.append(prefix_line)
        new_lines.append(line.new_line)
  else:
    new_lines.append(group.raw_line)

with open(os.path.join('pointer', 'transformed.txt'), 'w') as transformed_file:
  transformed_file.writelines(new_lines)
