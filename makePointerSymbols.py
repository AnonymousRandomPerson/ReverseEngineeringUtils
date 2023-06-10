import os, re
from dataclasses import dataclass
from typing import Dict, List, Any

start_address = 0x8380000
current_address = start_address
include_unaligned_pointers = True
min_address = start_address

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
}

@dataclass
class TargetRange:
  start: int
  end: int

target_pointer_ranges = [
  TargetRange(0x8380000, 0x83800c8),
  TargetRange(0x83801a4, 0x83801a8),
  TargetRange(0x83809b4, 0x83809b8),
  TargetRange(0x8380abc, 0x8380ac0),
  TargetRange(0x8382888, 0x838288c),
  TargetRange(0x8382c08, 0x8382c0c),
  TargetRange(0x8384918, 0x838491c),
  TargetRange(0x8384ca0, 0x8384ca4),
  TargetRange(0x8388ad4, 0x8388ad8),
  TargetRange(0x8388e54, 0x8388e58),
  TargetRange(0x838cf9c, 0x838cfa0),
  TargetRange(0x838d31c, 0x838d320),
  TargetRange(0x8391c4c, 0x8391c50),
  TargetRange(0x8391fcc, 0x8391fd0),
  TargetRange(0x83923a4, 0x83923a8),
  TargetRange(0x839263c, 0x8392640),
  TargetRange(0x8392b8c, 0x8392b90),
  TargetRange(0x8398aa0, 0x8398aa4),
  TargetRange(0x8399f88, 0x8399f8c),
  TargetRange(0x839a308, 0x839a30c),
  TargetRange(0x839b588, 0x839b58c),
  TargetRange(0x839b818, 0x839b81c),
  TargetRange(0x83a1578, 0x83a157c),
  TargetRange(0x83a2af8, 0x83a2afc),
  TargetRange(0x83801b0, 0x8380acc),
  TargetRange(0x8391fd8, 0x83923b4),
  TargetRange(0x83923b0, 0x839264c),
  TargetRange(0x8392648, 0x8392b64),
  TargetRange(0x839b354, 0x839b580),
  TargetRange(0x839b594, 0x839b7f0),
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
  if not joined_parts.startswith('.byte'):
    joined_parts = f'.byte {joined_parts.lstrip()}'
  add_bin_line(joined_parts)
  current_address += len(current_sections)
  current_sections = []

for line in raw_text:
  bin_size = 0
  current_bin_line_group = BinLineGroup(line, [])
  bin_line_groups.append(current_bin_line_group)

  if line.startswith('.byte'):
    comma_split = line.split(',')

    for part in comma_split:
      current_sections.append(part)
      if len(current_sections) >= 4:
        add_current_part()
        current_sections = []

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
    elif line.startswith('#include'):
      include_file = line[len('#include "') : -2]
      if include_file in include_sizes:
        bin_size += include_sizes[include_file]
      else:
        print('Found unknown #include:', include_file)

    add_bin_line(line)

    current_address += bin_size

print('End address:', hex(current_address))

replace_lines = []

used_ranges = set()
for line in bin_lines:
  if line.new_line.startswith('.byte'):
    match = re.search(r'(?:0x[0-f]{2}, ){3}0x0[89]', line.new_line)
    if match:
      split_bytes = match.group(0).split(', ')
      address = ''.join(reversed(split_bytes)).replace('0x', '').upper()[1:]
      address_int = int(f'0x{address}', 16)

      if len(target_pointer_ranges) == 0:
        in_target_range = True
      else:
        in_target_range = False
        for target_pointer_range in target_pointer_ranges:
          if line.address >= target_pointer_range.start and line.address <= target_pointer_range.end:
            in_target_range = True
            used_ranges.add(target_pointer_range.start)
            break

      if address_int <= current_address and address_int >= min_address and (include_unaligned_pointers or address_int % 4 == 0) and in_target_range:
        pointer_name = f'gUnknown_{address}'
        replace_lines.append(ReplaceLine(address_int, [f'.global {pointer_name}\n', f'{pointer_name}:\n']))
        line.new_line = f'{line.new_line[:match.start()]}{pointer_name}{line.new_line[match.end():]}'.replace('.byte', '.4byte')
        line.changed = True
      else:
        pass#print(f'Found possible pointer outside range at address {hex(line.address)}: {hex(address_int)}')

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
        byte_line = f'.byte {byte}\n'
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
        prefix_lines.append(prefix_line)
  else:
    missing_addresses.add(line.address)

for address in sorted(missing_addresses):
  print(f'Address {hex(address)} not found.')

new_lines = []

def combine_byte_string(current_byte_string: str):
  return f'.byte {", ".join(current_byte_string)}\n' 

for group in bin_line_groups:
  changed = any([bin_line.changed for bin_line in group.bin_lines])
  if changed:
    if group.raw_line.startswith('.byte'):
      current_byte_string: List[str] = []

      for line in group.bin_lines:
        if line.new_line.startswith('.4byte'):
          if len(current_byte_string) > 0:
            new_lines.append(combine_byte_string(current_byte_string))
            current_byte_string = []
          for prefix_line in line.prefix_lines:
            new_lines.append(prefix_line)
          new_lines.append(line.new_line)
        elif line.new_line.startswith('.byte'):
          if len(line.prefix_lines) > 0 and len(current_byte_string) > 0:
            new_lines.append(combine_byte_string(current_byte_string))
            current_byte_string = []
          for prefix_line in line.prefix_lines:
            new_lines.append(prefix_line)
          current_byte_string.append(line.new_line[6:-1])
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
