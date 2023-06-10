import os
from dataclasses import dataclass

start_address = 0x8380000
end_pointer_list = 0x83800C8

@dataclass
class TargetRange:
  start: int
  end: int

target_ranges = [TargetRange(start_address, end_pointer_list)]
sir0_headers = set()

with open(os.path.join('pointer', 'transformed_reference.txt'), 'r') as raw_file:
  raw_text = raw_file.readlines()

def create_pointer_search(line: str):
  return f'{line[7:-1]}:\n'

def extract_pointer_address(line: str):
  return int(line[9:16], 16)

def extract_size(line: str):
  return int(line[14:16] + line[8:10], 16)

num_sir0 = 431#extract_size(raw_text[1])
pointer_list = raw_text[6 : 6 + num_sir0 * 2]
for i in range(0, len(pointer_list), 2):
  pointer_line = pointer_list[i + 1]
  sir0_headers.add(create_pointer_search(pointer_line))

sir0_metadata = set()
for i, line in enumerate(raw_text):
  if line in sir0_headers:
    pointer_address = extract_pointer_address(line)
    target_ranges.append(TargetRange(pointer_address + 4, pointer_address + 8))
    sir0_metadata.add(create_pointer_search(raw_text[i + 2]))

for i, line in enumerate(raw_text):
  if line in sir0_metadata:
    pointer_address = extract_pointer_address(line)

    size_line = raw_text[i + 1]
    try:
      if size_line.startswith('.byte'):
        list_pointer = int(raw_text[i + 2][16:24], 16)
        target_ranges.append(TargetRange(list_pointer, pointer_address + 20))
      else:
        list_pointer = int(raw_text[i + 1][16:24], 16)
        target_ranges.append(TargetRange(list_pointer, pointer_address + 28))
    except ValueError:
      pass

for target_range in target_ranges:
  print(f'TargetRange({hex(target_range.start)}, {hex(target_range.end)}),')