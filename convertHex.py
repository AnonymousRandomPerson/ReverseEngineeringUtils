import os

with open(os.path.join('asm', 'raw.txt'), 'r') as raw_file:
  raw_text = raw_file.readlines()

for line in raw_text:
  print(int(line[:-1], 16))
