import json, os
from romUtils import GAME_FILE_PATH
from data.itemData import item_list
from generateUtils import *

item_categories = {
  0: 'CATEGORY_THROWN_LINE',
  1: 'CATEGORY_THROWN_ARC',
  2: 'CATEGORY_BERRIES_SEEDS_VITAMINS',
  3: 'CATEGORY_FOOD_GUMMIES',
  4: 'CATEGORY_HELD_ITEMS',
  5: 'CATEGORY_TMS_HMS',
  6: 'CATEGORY_POKE',
  8: 'CATEGORY_OTHER',
  9: 'CATEGORY_ORBS',
  10: 'CATEGORY_LINK_BOX',
  11: 'CATEGORY_USED_TM'
}

item_action_types = {
  0: 'ITEM_ACTION_TYPE_NOTHING',
  1: 'ITEM_ACTION_TYPE_THROWABLE',
  2: 'ITEM_ACTION_TYPE_ROCKS',
  3: 'ITEM_ACTION_TYPE_RIBBONS',
  4: 'ITEM_ACTION_TYPE_FOOD',
  5: 'ITEM_ACTION_TYPE_HEALING',
  6: 'ITEM_ACTION_TYPE_CHESTNUT',
  7: 'ITEM_ACTION_TYPE_MONEY_WISH_STONE',
  8: 'ITEM_ACTION_TYPE_MISC',
  9: 'ITEM_ACTION_TYPE_TM',
  10: 'ITEM_ACTION_TYPE_LINK_BOX',
  11: 'ITEM_ACTION_TYPE_SPECS',
  12: 'ITEM_ACTION_TYPE_SCARFS',
  13: 'ITEM_ACTION_TYPE_ORBS'
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
    item_json['category'] = item_categories[read_u8(game_file)]
    item_json['spriteID'] = read_u8(game_file)
    read_u16(game_file)
    item_json['description'] = read_pointer(game_file)
    assign_nondefault(item_json, 'aiFlags', read_bool8_array(game_file, 3))
    read_u8(game_file)
    assign_nondefault(item_json, 'moveID', get_move_macro(read_u16(game_file)))
    item_json['order'] = read_u8(game_file)
    assign_nondefault(item_json, 'unkThrow1B', read_u8_array(game_file, 2))
    item_json['paletteID'] = read_u8(game_file)
    item_json['actionType'] = item_action_types[read_u8(game_file)]
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
  generate_string_file(game_file, item_json_array, 'item_descriptions.s', [JsonStringField('description', 'ItemDescription', replace_names)],align=False)

  for item_json in item_json_array:
    item_json['name'] = item_json['namePointer']
    del item_json['namePointer']

with open(os.path.join('json', 'item_data.json'), 'w') as json_file:
  json_file.write(json.dumps(item_json_array, indent=4, ensure_ascii=False) + '\n')
