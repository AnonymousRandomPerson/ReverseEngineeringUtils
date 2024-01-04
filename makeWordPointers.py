import os
from typing import Set

start_address = 0x02000000
end_address = 0x02400000
# start_address = 0x037F8000
# end_address = 0x0380b488
# start_address = 0x027E0000
# end_address = 0x027F91E0
prefix_addresses = [
  # (0x022BCA80, 'ov00'),
  # (0x02329520, 'ov01'),
  # (0x02329520, 'ov02'),
  # (0x0233CA80, 'ov03'),
  # (0x0233CA80, 'ov04'),
  # (0x0233CA80, 'ov05'),
  # (0x0233CA80, 'ov06'),
  # (0x0233CA80, 'ov07'),
  # (0x0233CA80, 'ov08'),
  # (0x0233CA80, 'ov09'),
  # (0x022BCA80, 'ov10'),
  # (0x022DC240, 'ov11'),
  # (0x0238A140, 'ov13'),
  # (0x0238A140, 'ov14'),
  # (0x0238A140, 'ov15'),
  # (0x0238A140, 'ov16'),
  # (0x0238A140, 'ov17'),
  # (0x0238A140, 'ov18'),
  # (0x0238A140, 'ov19'),
  # (0x0238A140, 'ov20'),
  # (0x0238A140, 'ov21'),
  # (0x0238A140, 'ov22'),
  # (0x0238A140, 'ov23'),
  # (0x0238A140, 'ov24'),
  # (0x0238A140, 'ov25'),
  # (0x0238A140, 'ov26'),
  # (0x0238A140, 'ov27'),
  # (0x0238A140, 'ov28'),
  # (0x022DC240, 'ov29'),
  # (0x02382820, 'ov30'),
  # (0x02382820, 'ov31'),
  # (0x022DC240, 'ov34'),
]

pointer_suffix = '_JP'

with open(os.path.join('pointer', 'raw.txt'), 'r') as raw_file:
  raw_text = raw_file.readlines()

in_range_addresses: Set[int] = set()
out_of_range_addresses: Set[int] = set()
WORD_SEARCH = '.word 0x'
for i, line in enumerate(raw_text):
  if WORD_SEARCH in line and len(line) > len(WORD_SEARCH) + 8 and '+' not in line or '=0x0' in line:
    address_string = line[-9:-1]
    address = int(address_string, 16)
    if address >= start_address and address <= end_address:
      replace_prefix = '_'
      for prefix_address in reversed(prefix_addresses):
        if address >= prefix_address[0]:
          replace_prefix = prefix_address[1] + replace_prefix
          break
      raw_text[i] = line.replace(f'0x{address_string}', f'{replace_prefix}{address_string}{pointer_suffix}')
      in_range_addresses.add(address)
    else:
      out_of_range_addresses.add(address)


print('Addresses in range:')
for address in sorted(in_range_addresses):
  print(hex(address))

print('\nAddresses out of range:')
for address in sorted(out_of_range_addresses):
  print(hex(address))

with open(os.path.join('pointer', 'transformed.txt'), 'w') as transformed_file:
  transformed_file.writelines(raw_text)
