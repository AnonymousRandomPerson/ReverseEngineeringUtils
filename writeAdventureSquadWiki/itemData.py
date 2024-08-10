from enum import Enum, auto

class ItemCategory(Enum):
  POKE = auto()
  SCARF = auto()
  SPECS = auto()
  ROCK = auto()
  SPIKE = auto()
  FOOD = auto()
  GUMMI = auto()
  BERRY = auto()
  SEED = auto()
  DRINK = auto()
  EVOLUTION = auto()
  TM = auto()
  ORB = auto()

FOOD_ITEMS = set([
  'Apple',
  'Big Apple',
  'Grimy Food',
  'Banana',
  'Chestnut',
  'Bitter Chocolate',
  'White Chocolate',
  'Sweet Chocolate',
])

ROCK_ITEMS = set([
  'Geo Pebble',
  'Gravelerock',
  'Gone Pebble',
  'Gravelyrock',
])

SPIKE_ITEMS = set([
  'Stick',
  'Iron Thorn',
  'Silver Spike',
])

DRINK_ITEMS = set([
  'Max Elixir',
  'Mix Elixir',
  'Team Elixir',
  'Calcium',
  'Ginseng',
  'Iron',
  'Protein',
  'Zinc',
])

LOOKALIKE_ITEMS = set([
  'Dough Seed',
  'Dropeye Seed',
  'Gaggle Specs',
  'Gone Pebble',
  'Gravelyrock',
  'Mix Elixir',
  'No-Slip Cap',
  'Oren Berry',
  'Reviser Seed',
  'Slip Seed',
  'Via Seed',
  'Wander Gummi',
  'Y-Ray Specs',
])

TM_MOVES = set([
  'Focus Punch',
  'Dragon Claw',
  'Water Pulse',
  'Calm Mind',
  'Roar',
  'Toxic',
  'Bulk Up',
  'Bullet Seed',
  'Hidden Power',
  'Taunt',
  'Ice Beam',
  'Blizzard',
  'Hyper Beam',
  'Light Screen',
  'Protect',
  'Giga Drain',
  'Safeguard',
  'Frustration',
  'SolarBeam',
  'Iron Tail',
  'Thunderbolt',
  'Thunder',
  'Earthquake',
  'Return',
  'Dig',
  'Psychic',
  'Shadow Ball',
  'Brick Break',
  'Reflect',
  'Shock Wave',
  'Flamethrower',
  'Sludge Bomb',
  'Fire Blast',
  'Aerial Ace',
  'Torment',
  'Facade',
  'Secret Power',
  'Rest',
  'Attract',
  'Thief',
  'Steel Wing',
  'Skill Swap',
  'Overheat',
  'Roost',
  'Focus Blast',
  'Energy Ball',
  'False Swipe',
  'Brine',
  'Fling',
  'Charge Beam',
  'Endure',
  'Dragon Pulse',
  'Drain Punch',
  'Will-O-Wisp',
  'Silver Wind',
  'Embargo',
  'Explosion',
  'Shadow Claw',
  'Payback',
  'Recycle',
  'Giga Impact',
  'Rock Polish',
  'Flash',
  'Stone Edge',
  'Avalanche',
  'Thunder Wave',
  'Gyro Ball',
  'Swords Dance',
  'Stealth Rock',
  'Psych Up',
  'Captivate',
  'Dark Pulse',
  'Rock Slide',
  'X-Scissor',
  'Sleep Talk',
  'Natural Gift',
  'Poison Jab',
  'Dream Eater',
  'Grass Knot',
  'Swagger',
  'Pluck',
  'U-turn',
  'Substitute',
  'Flash Cannon',
  'Trick Room',
  'Dive',
  'Vacuum-Cut',
  'Wide Slash',
])

def get_item_category(item: str):
  if item == 'Poké':
    return ItemCategory.POKE
  if item.endswith('Berry'):
    return ItemCategory.BERRY
  if item in FOOD_ITEMS:
    return ItemCategory.FOOD
  if item.endswith('Orb'):
    return ItemCategory.ORB
  if item.endswith('Seed'):
    return ItemCategory.SEED
  if item.endswith('Gummi'):
    return ItemCategory.GUMMI
  if item in DRINK_ITEMS:
    return ItemCategory.DRINK
  if item in ROCK_ITEMS:
    return ItemCategory.ROCK
  if item in SPIKE_ITEMS:
    return ItemCategory.SPIKE
  if item.endswith('Band') or item.endswith('Belt') or item.endswith('Cap') or item.endswith('Ribbon') or item.endswith('Scarf'):
    return ItemCategory.SCARF
  if item.endswith('Lens') or item.endswith('scope') or item.endswith('Specs'):
    return ItemCategory.SPECS
  if item in TM_MOVES:
    return ItemCategory.TM
  raise ValueError('Unknown category for item: ' + item)

def get_item_link(item: str):
  if item == 'Stick':
    return 'Throwing item'
  if item in LOOKALIKE_ITEMS:
    return 'Lookalike Item'

  category = get_item_category(item)
  if category == ItemCategory.FOOD:
    return 'Food (Mystery Dungeon)'
  if category == ItemCategory.BERRY:
    return 'Berry'
  if category == ItemCategory.ORB:
    return 'Wonder Orb'
  if category == ItemCategory.SEED:
    return 'Seed'
  if category == ItemCategory.DRINK:
    return 'Health drink'
  if category == ItemCategory.TM:
    return 'TM'
  if category == ItemCategory.SCARF:
    return 'Scarf (Mystery Dungeon)'
  if category == ItemCategory.SPECS:
    return 'Glasses'

def get_item_sprite(item: str):
  if item == 'Poké':
    return 'Poké currency'
  if 'Apple' in item:
    return 'MDBag Apple TDS Sprite'
  if item == 'Stick':
    return 'MDBag Stick TDS Sprite'
  if item.lower().endswith('scope'):
    return 'MDBag Scope TDS Sprite'
  if item.endswith('Specs'):
    return 'MDBag Glasses TDS Sprite'
  if item.endswith('Chocolate'):
    return 'MDBag Sweet Chocolate Sprite'
  if item in LOOKALIKE_ITEMS:
    if item.endswith('Seed'):
      return 'MDBag Seed TDS Sprite'
    if item.endswith('Specs'):
      return 'MDBag Glasses TDS Sprite'
    if item == 'Oren Berry':
      return 'MDBag Oran Berry Sprite'
    if item == 'Gone Pebble':
      return 'MDBag Geo Pebble TDS Sprite'
    if item == 'Gravelyrock':
      return 'MDBag Gravelerock TDS Sprite'
    if item == 'No-Slip Cap':
      return 'MDBag Scarf TDS Sprite'
    if item == 'Wander Gummi':
      return 'MDBag Wonder Gummi TDS Sprite'

  category = get_item_category(item)
  if category == ItemCategory.BERRY or category == ItemCategory.FOOD or item == 'Scope Lens':
    return f'MDBag {item} Sprite'
  if category == ItemCategory.DRINK:
    return 'MDBag Drink TDS Sprite'
  if category == ItemCategory.SCARF:
    return 'MDBag Scarf Sprite'