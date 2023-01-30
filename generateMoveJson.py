import json, os
from romUtils import GAME_FILE_PATH
from data.moveData import move_list
from data.typeData import type_map
from generateUtils import *

with open(GAME_FILE_PATH, 'rb') as game_file:
  game_file.seek(0x3679A0)

  move_json_array = []

  for move in move_list:
    move_json = {}
    move_json['name'] = move
    move_json['namePointer'] = read_pointer(game_file)
    # move_json['address'] = get_current_address(game_file)
    move_json['basePower'] = read_u8(game_file)
    read_u8(game_file)
    move_json['type'] = type_map[read_u8(game_file)]
    read_u8(game_file)
    move_json['targetingFlags'] = read_binary16(game_file)
    move_json['aiTargetingFlags'] = read_binary16(game_file)
    move_json['basePP'] = read_u8(game_file)
    move_json['aiWeight'] = read_u8(game_file)
    move_json['accuracy1'] = read_u8(game_file)
    move_json['accuracy2'] = read_u8(game_file)
    move_json['aiConditionRandomChance'] = read_u8(game_file)
    move_json['hitCount'] = read_u8(game_file)
    assign_nondefault(move_json, 'maxUpgradeLevel', read_u8(game_file))
    assign_nondefault(move_json, 'criticalHitChance', read_u8(game_file))
    assign_nondefault(move_json, 'affectedByMagicCoat', read_bool8(game_file))
    assign_nondefault(move_json, 'targetsUser', read_bool8(game_file))
    assign_nondefault(move_json, 'usesMouth', read_bool8(game_file))
    move_json['cannotHitFrozen'] = read_bool8(game_file)
    assign_nondefault(move_json, 'dealsDirectDamage', read_bool8(game_file))
    move_json['rangeType'] = read_u8(game_file)
    read_u16(game_file)
    move_json['description'] = read_pointer(game_file)
    move_json['useText'] = read_pointer(game_file)

    move_json_array.append(move_json)

  replace_names_name = {
    'Iswatching': 'IsWatching',
    'Regularattack': 'RegularAttack',
    '$$$': 'Placeholder',
  }
  replace_names_description = {
    'AirCutter': 'HighCritical',
    'Aromatherapy': 'HealTeamStatus',
    'Astonish': 'Cringe',
    'Bubble': 'LowerSpeedChanceDistance',
    'BulletSeed': 'MultiHitDistance',
    'Clamp': 'Constriction',
    'Confusion': 'ConfuseChance',
    'Crunch': 'LowerSpecialDefenseChance',
    'Disable': 'Paralyze',
    'DoomDesire': 'FixedDamage',
    'DoubleKick': 'HitTwice',
    'Doubleslap': 'MultiHit',
    'DoubleTeam': 'BoostEvasion',
    'Extremespeed': 'TwoTilesAhead',
    'FlameWheel': 'BurnChance',
    'GigaDrain': 'Drain',
    'Grasswhistle': 'Sleep',
    'Harden': 'BoostDefense',
    'HornDrill': 'OneHit',
    'IceBall': 'MultiHitUntilMiss',
    'IronDefense': 'BoostDefenseTwo',
    'IronTail': 'LowerDefenseChance',
    'Iswatching': 'IsWatching',
    'PoisonGas': 'Poison',
    'PowderSnow': 'FreezeChanceRoom',
    'Psybeam': 'ConfuseChanceDistance',
    'Pursuit': 'Counter',
    'RazorLeaf': 'HighCriticalDistance',
    'Regularattack': 'Null',
    'RockThrow': 'Damage',
    'RockTomb': 'DamageLowerSpeed',
    'SandAttack': 'LowerAccuracy',
    'ScaryFace': 'LowerSpeed',
    'ShadowPunch': 'NeverMiss',
    'Sharpen': 'BoostAttack',
    'Smog': 'PoisonChance',
    'SpiderWeb': 'LegHolder',
    'Submission': 'Recoil',
    'Supersonic': 'Confuse',
    'TailWhip': 'LowerDefense',
    'Thunderpunch': 'ParalyzeChance',
    '$$$': 'Placeholder',
  }
  replace_names_use = {
    'Bide2': 'Bide',
    'IronTail': 'Use',
    'Regularattack': 'RegularAttack',
  }
  skip_names = {
    'Wish': 'SpeciesCategoryJirachi',
    'Bounce': 'SpeciesCategorySpoink',
    'Meditate': 'SpeciesCategoryMeditite',
    'ArmThrust': 'SpeciesCategoryHariyama',
    'Swallow': 'SpeciesCategorySwellow',
    'Bite': 'SpeciesCategoryPoochyena',
    'Thunder': 'SpeciesCategoryRaikou',
    'Screech': 'SpeciesCategoryMisdreavus',
    'Moonlight': 'SpeciesCategoryUmbreon',
    'Transform': 'SpeciesCategoryDitto',
    'Barrier': 'SpeciesCategoryMrMime',
    'Spikes': 'SpeciesCategoryRhyhorn',
    'PoisonGas': 'SpeciesCategoryKoffing',
    'Hypnosis': 'SpeciesCategoryDrowzee',
    'Sludge': 'SpeciesCategoryGrimer',
    'Superpower': 'SpeciesCategoryMachop',
    'Eruption': 'SpeciesCategoryNone',
  }
  fields = [
    JsonStringField('namePointer', 'MoveName', replace_names_name, skip_names),
    JsonStringField('description', 'MoveDescription', replace_names_description),
    JsonStringField('useText', 'MoveUseText', replace_names_use),
  ]
  generate_string_file(game_file, move_json_array, 'move_names.s', fields)

  for move_json in move_json_array:
    move_json['name'] = move_json['namePointer']
    del move_json['namePointer']

with open(os.path.join('json', 'move_data.json'), 'w') as json_file:
  json_file.write(json.dumps(move_json_array, indent=4) + '\n')
