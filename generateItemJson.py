import json, os
from romUtils import GAME_FILE_PATH
from data.itemData import item_list
from generateUtils import *

item_types = {
  0: 'ITEM_TYPE_THROWABLE',
  1: 'ITEM_TYPE_ROCK',
  2: 'ITEM_TYPE_BERRY_SEED',
  3: 'ITEM_TYPE_APPLE_GUMMI',
  4: 'ITEM_TYPE_HOLD_ITEM',
  5: 'ITEM_TYPE_TM',
  6: 'ITEM_TYPE_MONEY',
  8: 'ITEM_TYPE_MISC',
  9: 'ITEM_TYPE_ORB',
  10: 'ITEM_TYPE_LINK_BOX',
  11: 'ITEM_TYPE_USED_TM'
}

item_categories = {
  0: 'ITEM_CATEGORY_NOTHING',
  1: 'ITEM_CATEGORY_THROWABLE',
  2: 'ITEM_CATEGORY_ROCKS',
  3: 'ITEM_CATEGORY_RIBBONS',
  4: 'ITEM_CATEGORY_FOOD',
  5: 'ITEM_CATEGORY_HEALING',
  6: 'ITEM_CATEGORY_CHESTNUT',
  7: 'ITEM_CATEGORY_MONEY_WISH_STONE',
  8: 'ITEM_CATEGORY_MISC',
  9: 'ITEM_CATEGORY_TM',
  10: 'ITEM_CATEGORY_LINK_BOX',
  11: 'ITEM_CATEGORY_SPECS',
  12: 'ITEM_CATEGORY_SCARFS',
  13: 'ITEM_CATEGORY_ORBS'
}

with open(GAME_FILE_PATH, 'rb') as game_file:
  game_file.seek(0x30CC28)

  item_json_array = []

  for item in item_list:
    item_json = {}
    item_json['name'] = item
    item_json['namePointer'] = read_pointer(game_file)
    item_json['buyPrice'] = read_s32(game_file)
    item_json['sellPrice'] = read_s32(game_file)
    item_json['type'] = item_types[read_u8(game_file)]
    item_json['icon'] = read_u8(game_file)
    read_u16(game_file)
    item_json['descriptionPointer'] = read_pointer(game_file)
    assign_nondefault(item_json, 'aiFlags', read_bool8_array(game_file, 3))
    read_u8(game_file)
    assign_nondefault(item_json, 'move', get_move_macro(read_u16(game_file)))
    item_json['order'] = read_u8(game_file)
    assign_nondefault(item_json, 'unkThrow1B', read_u8_array(game_file, 2))
    item_json['palette'] = read_u8(game_file)
    item_json['category'] = item_categories[read_u8(game_file)]
    read_u8(game_file)

    item_json_array.append(item_json)

  generate_string_file(game_file, item_json_array, 'item_names.s', [JsonStringField('namePointer', 'ItemName')])
  replace_names = {
    'Stick': 'Spike',
    'Gravelerock': 'Rock',
    'KingsRock': 'EvolutionItemMulti',
    'Upgrade': 'EvolutionItemSingle',
    'BeatupOrb': 'Placeholder'
  }
  generate_string_file(game_file, item_json_array, 'item_descriptions.s', [JsonStringField('descriptionPointer', 'ItemDescription', replace_names)],align=False)

with open(os.path.join('json', 'item_data.json'), 'w') as json_file:
  json_file.write(json.dumps(item_json_array, indent=4, ensure_ascii=False) + '\n')
