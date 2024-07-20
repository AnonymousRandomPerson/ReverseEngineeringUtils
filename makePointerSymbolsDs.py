import os, re
from dataclasses import dataclass, field
from typing import Dict, List, Any

start_address = 0x02000BC4 # crt0
start_address = 0x020908D4 # main
start_address = 0x02317F44 # ov00
start_address = 0x0233AE78 # ov01
start_address = 0x0234FBC8 # ov02
start_address = 0x02346738 # ov03
start_address = 0x0233F568 # ov04
start_address = 0x0233FB4C # ov05
start_address = 0x0233ED04 # ov06
start_address = 0x023418BC # ov07
start_address = 0x0233E8AC # ov08
start_address = 0x0233F56C # ov09
start_address = 0x022C4394 # ov10
start_address = 0x02316A3C # ov11
start_address = 0x0238C010 # ov13
start_address = 0x0238D96C # ov14
start_address = 0x0238AF54 # ov15
start_address = 0x0238CD08 # ov16
start_address = 0x0238BA80 # ov17
start_address = 0x0238D208 # ov18
start_address = 0x0238D68C # ov19
start_address = 0x0238CF7C # ov20
start_address = 0x0238CA28 # ov21
start_address = 0x0238E81C # ov22
start_address = 0x0238D2E8 # ov23
start_address = 0x0238C508 # ov24
start_address = 0x0238B498 # ov25
start_address = 0x0238AE20 # ov26
start_address = 0x0238C948 # ov27
start_address = 0x0238ACFC # ov28
start_address = 0x0234FCFC # ov29
start_address = 0x02386080 # ov30
start_address = 0x02389D94 # ov31
start_address = 0x022DCFF4 # ov34
start_address = 0x027F7184 # arm7
start_address = 0x038074E0 # arm7 wram

start_address = 0x02090C6C # main EU
start_address = 0x02318758 # ov00 EU
start_address = 0x0233B5C4 # ov01 EU
start_address = 0x023503F4 # ov02 EU
start_address = 0x02340340 # ov07 EU
start_address = 0x0233F038 # ov08 EU
start_address = 0x022C4CE8 # ov10 EU
start_address = 0x0231741C # ov11 EU
start_address = 0x02350908 # ov29 EU

start_address = 0x02090BBC # main JP
start_address = 0x023196F0 # ov00 JP
start_address = 0x0233C6F8 # ov01 JP
start_address = 0x02347FC8 # ov03 JP
start_address = 0x023413D4 # ov05 JP
start_address = 0x0234013C # ov08 JP
start_address = 0x022C5A7C # ov10 JP
start_address = 0x02317FA0 # ov11 JP
start_address = 0x02350F7C # ov29 JP

start_address = 0x023413D4 # ov05 JP

REGION_US = 'US'
REGION_EU = 'EU'
REGION_JP = 'JP'
REGION_MACROS = {
  'US': REGION_US,
  'EUROPE': REGION_EU,
  'JAPAN': REGION_JP,
}

region = REGION_US

pointer_prefix = ''
pointer_suffix = ''
if region == REGION_EU:
  pointer_suffix = '_EU'
elif region == REGION_JP:
  pointer_suffix = '_JP'

current_address = start_address
include_unaligned_pointers = True
min_address = start_address
end_address = None
trailing_spaces = '\t'
name_custom_functions = False
autodetect_pointers = True

min_address = 0x02000000
end_address = 0x02400000

custom_pointers = set([
])

@dataclass
class TargetRange:
  start: int
  end: int


target_pointer_ranges = [
]

@dataclass
class RegionContainer:
  active_regions: List[str] = field(default_factory=list)
  past_regions: List[str] = field(default_factory=list)

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
bss_address = None
existing_labels = set()

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

SPACE_FIND = '.space '

current_regions: List[RegionContainer] = []
def get_top_level_regions() -> List[str]:
  if len(current_regions) <= 1:
    return []
  return current_regions[0].active_regions + current_regions[0].past_regions
for line in raw_text:
  line_strip = line.lstrip()
  bin_size = 0
  current_bin_line_group = BinLineGroup(line, [])
  bin_line_groups.append(current_bin_line_group)

  if line_strip.startswith('#if'):
    new_region = RegionContainer()
    current_regions.append(new_region)
    for region_name, region_key in REGION_MACROS.items():
      if f'ifdef {region_name}' in line_strip or f' defined({region_name})' in line_strip:
        new_region.active_regions.append(region_key)
      elif f'ifndef {region_name}' in line_strip or f'!defined({region_name})' in line_strip:
        new_region.active_regions.extend([region_key_2 for region_key_2 in REGION_MACROS.values() if region_key_2 != region_key and region_key_2 not in get_top_level_regions()])
  elif line_strip.startswith('#elif') or line_strip.startswith('#else'):
    current_region = current_regions[-1]
    current_region.past_regions.extend(current_region.active_regions)
    current_region.active_regions = []
    if line_strip.startswith('#else'):
      current_region.active_regions.extend([region_key for region_key in REGION_MACROS.values() if region_key not in current_region.past_regions and region_key not in get_top_level_regions()])
    else:
      for region_name, region_key in REGION_MACROS.items():
        if f' defined({region_name})' in line_strip:
          current_region.active_regions.append(region_key)
        elif f'!defined({region_name})' in line_strip:
          current_region.active_regions.extend([region_key_2 for region_key_2 in REGION_MACROS.values() if region_key_2 != region_key and region_key_2 not in current_region.past_regions and region_key_2 not in get_top_level_regions()])
  elif line_strip.startswith('#endif'):
    current_regions.pop()

  current_region = None
  if len(current_regions) > 0:
    current_region = current_regions[-1]

  if current_region is None or region in current_region.active_regions:
    # if ':' in line_strip:
    #   print(line_strip[:-1], hex(current_address))
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
      if line_strip.startswith('.string'):
        bin_size = len(line_strip.split('"')[1].replace('\\0', '0').replace('\\n', 'n')) + 1
      elif line_strip.startswith('.hword') or line_strip.startswith('.short'):
        bin_size = 2 * (line_strip.count(',') + 1)
      elif line_strip.startswith('.word'):
        bin_size = 4 * (line_strip.count(',') + 1)
      elif line_strip.startswith('.align 4'):
        address_align = current_address % 4
        if address_align > 0:
          bin_size = 4 - address_align
      elif line_strip.startswith('.bss') or line_strip.startswith('.data'):
        bin_size = current_address % 0x20
        if bin_size > 0 or line_strip.startswith('.data'):
          bin_size = 0x20 - bin_size
        if line_strip.startswith('.bss'):
          bss_address = current_address + bin_size
      elif line_strip.startswith(SPACE_FIND):
        bin_size = int(line_strip[line_strip.index(SPACE_FIND) + len(SPACE_FIND) : -1], 16)
      elif line_strip.endswith(':\n'):
        existing_labels.add(current_address)

      add_bin_line(line)

  current_address += bin_size

print('End address:', hex(current_address))
print('Size:', hex(current_address - start_address))
if end_address is None:
  end_address = current_address

function_prefix = pointer_prefix
if function_prefix == '':
  function_prefix = 'sub'

replace_lines = []

used_ranges = set()
if autodetect_pointers:
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
      match = re.search(r'(?:0x[0-f]{2}, ){3}0x02', new_line_strip)
      if match:
        split_bytes = match.group(0).split(', ')
        address = ''.join(reversed(split_bytes)).replace('0x', '').upper()[1:]
        replace_line = lambda pointer_name : f'{new_line_strip[:match.start()]}{pointer_name}{new_line_strip[match.end():]}'.replace('.byte', '.word')

    if replace_line:
      address_int = int(f'0x{address}', 16)

      address_alignment = address_int % 4
      if (include_unaligned_pointers or address_alignment <= 1) and address_int not in existing_labels:
        in_data_range = address_int < end_address and address_int >= min_address
        potential_data_pointer = in_data_range and (address_alignment == 0 or include_unaligned_pointers)
        if potential_data_pointer or address_int in custom_pointers:
          pointer_name = f'{pointer_prefix}_{address_int:08X}{pointer_suffix}'
          if name_custom_functions and address_int in custom_pointers:
            pointer_name = function_prefix + pointer_name
          replace_lines.append(ReplaceLine(address_int, [f'{trailing_spaces}.global {pointer_name}\n', f'{pointer_name}:\n']))
          line.new_line = trailing_spaces + replace_line(pointer_name)
          line.changed = True
        elif address_alignment == 0 and not in_data_range:
          print(f'Found possible pointer outside range at address {hex(line.address)}: {hex(address_int)}')

for pointer in custom_pointers:
  if pointer in existing_labels:
    continue
  pointer_name = f'{pointer_prefix}_{pointer:08X}{pointer_suffix}'
  replace_lines.append(ReplaceLine(pointer, [f'{trailing_spaces}.global {pointer_name}\n', f'{pointer_name}:\n']))

print(f'Found {len(replace_lines)} pointers.')
missing_addresses = set()

for line in replace_lines:
  if bss_address is not None and line.address >= bss_address and line.address < current_address:
    if line.address in bin_line_memory_map and bin_line_memory_map[line.address].address == line.address:
      continue
    space_split_line = None
    bin_line_index = len(bin_lines)
    for bin_line in reversed(bin_lines):
      bin_line_index -= 1
      if bin_line.address < line.address and '.space' in bin_line.new_line:
        space_split_line = bin_line
        break
      if bin_line.address < bss_address:
        break

    if space_split_line is None:
      print('Could not find .bss line to split for ', line.address)
      continue

    new_line_offset = line.address - space_split_line.address
    space_split_size = int(space_split_line.new_line[space_split_line.new_line.index(SPACE_FIND) + len(SPACE_FIND) : -1], 16)
    space_split_line.new_line = f'{trailing_spaces}.space 0x{new_line_offset:X}\n'
    new_line = f'{trailing_spaces}.space 0x{space_split_size - new_line_offset:X}\n'
    new_pointer_name = f'{pointer_prefix}_{line.address:08X}{pointer_suffix}'
    new_bin_line = BinLine(line.address, new_line, new_line, [f'{trailing_spaces}.global {new_pointer_name}\n', f'{new_pointer_name}:\n'], False, space_split_line.group)
    space_split_line.group.bin_lines.insert(space_split_line.group.bin_lines.index(space_split_line) + 1, new_bin_line)
    bin_lines.insert(bin_line_index + 1, new_bin_line)
    bin_line_memory_map[line.address] = new_bin_line

  if line.address in bin_line_memory_map:
    pointer_line = bin_line_memory_map[line.address]
    if line.address != pointer_line.address:
      old_pointer_line = pointer_line
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
        elif new_address == old_pointer_line.address:
          new_line.prefix_lines = old_pointer_line.prefix_lines
          new_line.changed = old_pointer_line.changed
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
  return f'{trailing_spaces}.byte {", ".join(current_byte_string)}\n'

for group in bin_line_groups:
  if any([bin_line.changed for bin_line in group.bin_lines]):
    group_line_strip = group.raw_line.lstrip()
    if group_line_strip.startswith('.byte'):
      current_byte_string: List[str] = []

      for line in group.bin_lines:
        line_strip = line.new_line.lstrip()
        if line_strip.startswith('.word'):
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
