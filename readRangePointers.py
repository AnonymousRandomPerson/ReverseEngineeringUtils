from generateUtils import read_pointer
from romUtils import GAME_FILE_PATH

with open(GAME_FILE_PATH, 'rb') as game_file:
  read_pos = 0x10CC0C
  game_file.seek(read_pos)
  pointers = []
  while read_pos < 0x10CCCF:
    pointers.append(read_pointer(game_file))
    read_pos += 4

  for pointer in pointers:
    pointer_hex = int(pointer[4:], 16)
    game_file.seek(pointer_hex)
    pointer_string = ''

    character = None
    while character != b'\x00':
      character = game_file.read(1)
      if character != b'\x00':
        if character == b'\xe9':
          character = 'é'
        else:
          character = character.decode('utf-8')
          if character == '\n':
            character = '\\n'
        pointer_string += character
    print(pointer_string)
