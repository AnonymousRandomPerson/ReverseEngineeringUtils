import json, os
from romUtils import GAME_FILE_PATH
from data.abilityData import ability_map
from data.friendAreaData import friend_area_map
from data.typeData import type_map
from generateUtils import *

evolve_types = {
  0: 'EVOLVE_TYPE_NONE',
  1: 'EVOLVE_TYPE_LEVEL',
  2: 'EVOLVE_TYPE_IQ',
  3: 'EVOLVE_TYPE_ITEM',
  13: 'EVOLVE_TYPE_LINK_CABLE'
}

walkable_tiles = {
  0: None,
  2: 'WALKABLE_TILE_CHASM',
  3: 'WALKABLE_TILE_WALL',
  4: 'WALKABLE_TILE_LAVA',
  5: 'WALKABLE_TILE_WATER'
}

with open(GAME_FILE_PATH, 'rb') as game_file:
  game_file.seek(0x357B98)

  monster_json_array = []

  for i in range(len(monster_list)):
    monster_json = {}
    monster_json['name'] = monster_list[i]
    monster_json['species'] = read_pointer(game_file)
    monster_json['category'] = read_pointer(game_file)
    monster_json['overworldPalette'] = read_u8(game_file)
    monster_json['bodySize'] = read_u8(game_file)
    read_u16(game_file)
    monster_json['movementSpeed'] = read_s32(game_file)
    assign_nondefault(monster_json, 'dialogueSprites', read_binary16(game_file))
    assign_nondefault(monster_json, 'unk12', read_bool8(game_file))
    monster_json['types'] = [type_map[t] for t in read_u8_array(game_file, 2) if t != 0]
    assign_nondefault(monster_json, 'movementType', walkable_tiles[read_u8(game_file)])
    monster_json['friend_area'] = friend_area_map[read_u8(game_file)]
    monster_json['abilities'] = [ability_map[a] for a in read_u8_array(game_file, 2) if a != 0]
    monster_json['shadowSize'] = read_u8(game_file)
    assign_nondefault(monster_json, 'unk1A', read_u8(game_file))
    monster_json['regenSpeed'] = read_u8(game_file)
    monster_json['canMove'] = read_bool8(game_file)
    monster_json['chanceAsleep'] = read_u8(game_file)
    monster_json['baseHP'] = read_u16(game_file)
    monster_json['expYield'] = read_s32(game_file)
    monster_json['baseAtkSpAtk'] = read_u16_array(game_file, 2)
    monster_json['baseDefSpDef'] = read_u16_array(game_file, 2)
    monster_json['weight'] = read_u16(game_file)
    monster_json['size'] = read_u16(game_file)
    monster_json['unk30'] = read_u8(game_file)
    monster_json['unk31'] = read_u8(game_file)
    monster_json['unk32'] = read_u8(game_file)
    monster_json['toolboxEnabled'] = read_bool8(game_file)

    evolve_from = read_u16(game_file)
    evolve_type = read_u16(game_file)
    if evolve_from != 0:
      monster_json['preEvolution'] = {}
      monster_json['preEvolution']['evolveFrom'] = get_monster_macro(evolve_from)
      monster_json['preEvolution']['evolveType'] = evolve_types[evolve_type]

    main_requirement = read_u16(game_file)
    additional_requirement = read_u16(game_file)
    if evolve_from != 0:
      monster_json['evolutionRequirements'] = {}
      if evolve_type == 3:
        monster_json['evolutionRequirements']['mainRequirement'] = get_item_macro(main_requirement)
      else:
        monster_json['evolutionRequirements']['additionalRequirement'] = main_requirement
      assign_nondefault(monster_json['evolutionRequirements'], 'additionalRequirement', additional_requirement)

    monster_json['dexInternal'] = read_u16_array(game_file, 2)
    monster_json['recruitRate'] = read_s16(game_file)
    monster_json['alphabetParent'] = read_u16_array(game_file, 2)
    read_u16(game_file)

    monster_json_array.append(monster_json)

  replace_names = {
    'UnownA': 'Unown'
  }
  generate_string_file(game_file, monster_json_array, 'monster_names.s', [JsonStringField('species', 'MonsterName', replace_names), JsonStringField('category', 'MonsterCategory', replace_names)], )

  for monster_json in monster_json_array:
    monster_json['name'] = monster_json['species']
    del monster_json['species']

with open(os.path.join('json', 'monster_data.json'), 'w') as json_file:
  json_file.write(json.dumps(monster_json_array, indent=4, ensure_ascii=False) + '\n')
