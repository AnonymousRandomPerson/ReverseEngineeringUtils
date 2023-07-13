import os
from typing import List
from filePaths import GAME_FILE_PATH

def read_incbin(offset: int, read_size: int) -> List[str]:
  new_lines = []
  with open(GAME_FILE_PATH, 'rb') as game_file:
    game_file.seek(offset)
    line = ''
    for i in range(read_size):
      if i % 16 == 0:
        if len(line) > 0:
          new_lines.append(line[:-2] + '\n')
        line = '.byte '
      
      data = game_file.read(1)
      field_value = int.from_bytes(data, 'little')
      field_value = format(field_value, '0%sx' % 2)
      line += f'0x{field_value}, '
    new_lines.append(line[:-2] + '\n')
  return new_lines

if __name__ == '__main__':
  offset = 0xF8988
  read_size = 0xC

  new_lines = read_incbin(offset, read_size)

  with open(os.path.join('pointer', 'transformed_reference.txt'), 'w') as transformed_file:
    transformed_file.writelines(new_lines)