import os

with open(os.path.join('pointer', 'raw.txt'), 'r') as raw_file:
  raw_text = raw_file.readlines()

pointers = []
used_pointers = set()
for line in raw_text:
  if line.startswith('.global'):
    pointers.append(line[len('.global '):-1])
  elif line.startswith('.4byte'):
    used_pointers.add(line[len('.4byte '):-1])

for pointer in pointers:
  if pointer not in used_pointers:
    print(pointer)
