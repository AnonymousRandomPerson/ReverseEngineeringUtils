import os

start_address = 0x380000
current_address = start_address

with open(os.path.join('pointer', 'raw.txt'), 'r') as raw_file:
  raw_text = raw_file.readlines()

def upper_hex(address):
  hex_string = hex(address)
  return f'0x{hex_string[2:].upper()}'

new_text = []
current_incbin_start = None
for line in raw_text:
  bin_size = 0
  if line.startswith('.byte'):
    bin_size = line.count('0x')
    if current_incbin_start is None:
      current_incbin_start = current_address
  else:
    if current_incbin_start is not None:
      new_text.append(f'.incbin "baserom.gba", {upper_hex(current_incbin_start)}, {upper_hex(current_address - current_incbin_start)}\n')
      current_incbin_start = None

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
    
    new_text.append(line)
  
  current_address += bin_size

if current_incbin_start is not None:
  new_text.append(f'.incbin "baserom.gba", {upper_hex(current_incbin_start)}, {upper_hex(current_address - current_incbin_start)}\n')

with open(os.path.join('pointer', 'transformed.txt'), 'w') as transformed_file:
  transformed_file.writelines(new_text)