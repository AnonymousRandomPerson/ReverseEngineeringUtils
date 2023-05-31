import os, struct
from data.b2w2ItemData import *

join_avenue_bin = os.path.join('bin', 'join_avenue.bin')

with open(join_avenue_bin, 'rb') as game_file:
  game_file.seek(0x33DEE4)
  for i in range(0x25):
    data = game_file.read(0x1A)

    print(f'{data[0]}-{data[2]}: {data[16]}%, {data[14]}')

def read_halfword(data, start):
  element = data[start : start + 2]
  return struct.unpack_from('<h', element)[0]

print()

with open(join_avenue_bin, 'rb') as game_file:
  game_file.seek(0x33E3B0)
  for i in range(12):
    data = game_file.read(0x2C)

    print(i)
    chance = 0
    for j in range(10):
      print(f'{item_map[read_halfword(data, (j * 2 + 3) * 2)]}: {data[(j * 2 + 2) * 2]}%')
    print()

