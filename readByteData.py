from filePaths import *
import os

overlay = '11'
# game_file_path = os.path.join(SKY_FOLDER, 'overlay', f'overlay_00{overlay}.bin')
# game_file_path = os.path.join(SKY_EU_FOLDER, 'overlay', f'overlay_00{overlay}.bin')
game_file_path = os.path.join(SKY_JP_FOLDER, 'overlay', f'overlay_00{overlay}.bin')
file_start = 0x02317FA0 - 0x022DD8E0
offset = file_start

data_size = 0x48B00 - file_start
read_size = 1

bytes_per_line = 16

byte_prefix = '\t.byte'

with open(game_file_path, 'rb') as game_file:
  game_file.seek(offset)
  full_data = byte_prefix
  for i in range(int(data_size / read_size)):
    data = game_file.read(read_size)
    field_value = int.from_bytes(data, 'little')
    field_value = format(field_value, '0%sx' % 2).upper()
    if i > 0:
      if i % bytes_per_line == 0:
        full_data += f'\n{byte_prefix}'
      else:
        full_data += ','
    full_data += ' 0x' + field_value

print(full_data)