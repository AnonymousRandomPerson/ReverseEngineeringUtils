import json, os
from romUtils import GAME_FILE_PATH
from data.dungeonData import dungeon_list
from generateUtils import *

with open(GAME_FILE_PATH, 'rb') as game_file:
  game_file.seek(0x109D30)

  dungeon_json_array = []

  for dungeon in dungeon_list:
    dungeon_json = {}
    dungeon_json['name'] = dungeon
    dungeon_json['stairDirectionUp'] = read_bool8(game_file)
    assign_nondefault(dungeon_json, 'unk1', read_bool8(game_file))
    dungeon_json['recruitingEnabled'] = read_bool8(game_file)
    dungeon_json['rescuesAllowed'] = read_s8(game_file)
    dungeon_json['maxItemsAllowed'] = read_u8(game_file)
    dungeon_json['maxPartyMembers'] = read_u8(game_file)
    assign_nondefault(dungeon_json, 'levelResetTo1', read_bool8(game_file))
    dungeon_json['keepMoney'] = read_bool8(game_file)
    assign_nondefault(dungeon_json, 'leaderCanSwitch', read_bool8(game_file))
    assign_nondefault(dungeon_json, 'hasCheckpoint', read_bool8(game_file))
    dungeon_json['enterWithoutGameSave'] = read_bool8(game_file)
    dungeon_json['HMMask'] = read_binary(game_file, 1)
    dungeon_json['turnLimit'] = read_s16(game_file)
    dungeon_json['randomMovementChance'] = read_s16(game_file)

    dungeon_json_array.append(dungeon_json)

with open(os.path.join('json', 'dungeon_data.json'), 'w') as json_file:
  json_file.write(json.dumps(dungeon_json_array, indent=4, ensure_ascii=False) + '\n')
