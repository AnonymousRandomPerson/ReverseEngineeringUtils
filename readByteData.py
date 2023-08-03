from filePaths import *
import os

game_file_path = os.path.join(SKY_FOLDER, 'arm9.bin')
file_start = 0
offset = 0xB7380 - file_start

data_size = 0xB73D8 - offset
read_size = 1

byte_prefix = '\t.byte'

with open(game_file_path, 'rb') as game_file:
  game_file.seek(offset)
  full_data = byte_prefix
  for i in range(int(data_size / read_size)):
    data = game_file.read(read_size)
    field_value = int.from_bytes(data, 'little')
    field_value = format(field_value, '0%sx' % 2).upper()
    if i > 0:
      if i % 16 == 0:
        full_data += f'\n{byte_prefix}'
      else:
        full_data += ','
    full_data += ' 0x' + field_value

print(full_data)