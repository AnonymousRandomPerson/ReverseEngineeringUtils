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

  species_json_array = []

  for i in range(len(species_list)):
    species_json = {}
    species_json['name'] = species_list[i]
    species_json['species'] = read_pointer(game_file)
    species_json['category'] = read_pointer(game_file)
    species_json['overworld_palette'] = read_u8(game_file)
    species_json['size'] = read_u8(game_file)
    read_u16(game_file)
    species_json['move_speed'] = read_s32(game_file)
    assign_nondefault(species_json, 'dialogue_sprites', read_binary16(game_file))
    assign_nondefault(species_json, 'unk12', read_bool8(game_file))
    species_json['types'] = [type_map[t] for t in read_u8_array(game_file, 2) if t != 0]
    assign_nondefault(species_json, 'walkable_tiles', walkable_tiles[read_u8(game_file)])
    species_json['friend_area'] = friend_area_map[read_u8(game_file)]
    species_json['abilities'] = [ability_map[a] for a in read_u8_array(game_file, 2) if a != 0]
    species_json['shadow_size'] = read_u8(game_file)
    assign_nondefault(species_json, 'unk1A', read_u8(game_file))
    species_json['unk1B'] = read_u8(game_file)
    species_json['isMoving'] = read_bool8(game_file)
    species_json['unk1D'] = read_u8(game_file)
    species_json['base_hp'] = read_u16(game_file)
    species_json['base_exp'] = read_s32(game_file)
    species_json['base_att_spatt'] = read_u16_array(game_file, 2)
    species_json['base_def_spdef'] = read_u16_array(game_file, 2)
    species_json['lowkick_dmg'] = read_u16(game_file)
    species_json['sizeorb_dmg'] = read_u16(game_file)
    species_json['unk30'] = read_u8(game_file)
    species_json['unk31'] = read_u8(game_file)
    species_json['unk32'] = read_u8(game_file)
    species_json['toolboxEnabled'] = read_bool8(game_file)

    evolve_from = read_u16(game_file)
    evolve_type = read_u16(game_file)
    if evolve_from != 0:
      species_json['pre'] = {}
      species_json['pre']['evolve_from'] = get_species_macro(evolve_from)
      species_json['pre']['evolve_type'] = evolve_types[evolve_type]

    evolve_need1 = read_u16(game_file)
    evolve_need2 = read_u16(game_file)
    if evolve_from != 0:
      species_json['needs'] = {}
      if evolve_type == 3:
        species_json['needs']['evolve_need1'] = get_item_macro(evolve_need1)
      else:
        species_json['needs']['evolve_need1'] = evolve_need1
      assign_nondefault(species_json['needs'], 'evolve_need2', evolve_need2)

    species_json['dexInternal'] = read_u16_array(game_file, 2)
    species_json['base_recruit'] = read_s16(game_file)
    species_json['alphabetParent'] = read_u16_array(game_file, 2)
    read_u16(game_file)

    species_json_array.append(species_json)

  replace_names = {
    'UnownA': 'Unown'
  }
  generate_string_file(game_file, species_json_array, 'species_names.s', [JsonStringField('species', 'SpeciesName', replace_names), JsonStringField('category', 'SpeciesCategory', replace_names)], )

with open(os.path.join('json', 'species_data.json'), 'w') as json_file:
  json_file.write(json.dumps(species_json_array, indent=4, ensure_ascii=False) + '\n')
