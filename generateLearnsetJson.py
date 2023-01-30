import json, os
from romUtils import GAME_FILE_PATH
from generateUtils import *
from data.monsterData import monster_map

def read_move_id(move_id, game_file):
  if move_id & 0x80:
    move_id_2 = read_u8(game_file)
    move_id = ((move_id & 0x7f) << 7) + move_id_2
  return move_id

with open(GAME_FILE_PATH, 'rb') as game_file:
  game_file.seek(0x360c06)

  learnset_json_array = []

  for i in range(len(monster_list) - 5):
    learnset_json = {
      'pokemon': strip_name(monster_map[i + 1], use_underscores=False),
      'levelUpMoves': [],
      'HMTMMoves': []
    }
    
    while move_id := read_u8(game_file):
      level_up_json = {}
      level_up_json['move'] = get_move_macro(read_move_id(move_id, game_file))
      level_up_json['level'] = read_u8(game_file)

      learnset_json['levelUpMoves'].append(level_up_json)

    while move_id := read_u8(game_file):
      learnset_json['HMTMMoves'].append(get_move_macro(read_move_id(move_id, game_file)))
      
    learnset_json_array.append(learnset_json)

  print(get_current_address(game_file))

with open(os.path.join('json', 'learnset_data.json'), 'w') as json_file:
  json_file.write(json.dumps(learnset_json_array, indent=4, ensure_ascii=False) + '\n')
