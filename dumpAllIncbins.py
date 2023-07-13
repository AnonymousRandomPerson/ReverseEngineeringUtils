import os

from dumpIncbin import read_incbin

with open(os.path.join('pointer', 'raw.txt'), 'r') as raw_file:
  raw_text = raw_file.readlines()
  
new_lines = []

for line in raw_text:
  line_strip = line.lstrip()
  if line_strip.startswith('.incbin'):
    new_lines.append(f'@ replacing {line_strip}')
    line_split = line.split(',')
    offset = int(line_split[1][1:], 16)
    read_size = int(line_split[2][1:-1], 16)
    new_lines.extend(read_incbin(offset, read_size))
  else:
    new_lines.append(line)

with open(os.path.join('pointer', 'transformed.txt'), 'w') as transformed_file:
  transformed_file.writelines(new_lines)