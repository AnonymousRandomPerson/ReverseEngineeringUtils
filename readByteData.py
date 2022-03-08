from filePaths import GAME_FILE_PATH

offset = 0xF522C
data_size = 0x288
read_size = 2

with open(GAME_FILE_PATH, 'rb') as game_file:
  game_file.seek(offset)
  full_data = '.byte'
  for i in range(int(data_size / read_size)):
    data = game_file.read(read_size)
    field_value = int.from_bytes(data, 'little')
    field_value = format(field_value, '0%sx' % 2)
    if i > 0:
      full_data += ','
    full_data += ' 0x' + field_value

print(full_data)