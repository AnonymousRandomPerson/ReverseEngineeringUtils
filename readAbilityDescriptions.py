from romUtils import GAME_FILE_PATH

with open(GAME_FILE_PATH, 'rb') as game_file:
  read_pos = 0x10BABC
  game_file.seek(read_pos)
  current_ability = ''
  last_character = ''
  while read_pos < 0x10CC0C:
    character = game_file.read(1)
    if character == b'\x00':
      if last_character != b'\x00':
        print(current_ability)
        current_ability = ''
    else:
      if character == b'\xe9':
        character = 'é'
      else:
        character = character.decode('utf-8')
        if character == '\n':
          character = '\\n'
      current_ability += character
    last_character = character
    read_pos += 1
