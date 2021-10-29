from romUtils import GAME_FILE_PATH

with open(GAME_FILE_PATH, 'rb') as game_file:
  read_pos = 0x10B97D
  ability_index = 1
  current_ability = ''
  while read_pos > 0x10B5FA:
    game_file.seek(read_pos)
    character = game_file.read(1)
    if character == b'\x00' or character == b'\x08':
      if len(current_ability) > 0:
        ability_hex = hex(ability_index).upper().replace('X', 'x')
        print(f'    ABILITY_{current_ability} = {ability_hex},')
        current_ability = ''
        ability_index += 1
    else:
      character = character.decode('utf-8')
      if character == ' ':
        character = '_'
      current_ability = character.upper() + current_ability
    read_pos -= 1
