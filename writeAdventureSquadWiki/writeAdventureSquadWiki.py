from dataclasses import dataclass
from pokemonData import *
from itemData import *

POKEMON_FILE = 'pokemon.txt'
ITEMS_FILE = 'items.txt'
SHOP_FILE = 'shop.txt'
MONSTER_HOUSE_FILE = 'monster_house.txt'

DEST_FILE = 'wiki.txt'

type_style = 'electric'
recruitable = True

@dataclass
class IntRange:
  start: int
  end: int

  def __str__(self) -> str:
    if self.start == self.end:
      return str(self.start)
    return f'{self.start}-{self.end}'

class PokemonInfo:
  name: str
  form: str = None
  metadata: PokemonMetadata
  levels: IntRange = None
  floors: list[IntRange]
  mystery_part: bool = False
  boss: bool = False

  def __init__(self, name: str):
    self.name, self.form = get_form(name)
    self.metadata = pokemon_metadata[self.name]
    self.floors = []

  def add_level(self, level: int):
    if self.levels is None:
      self.levels = IntRange(level, level)
    elif level < self.levels.start:
      self.levels = IntRange(level, self.levels.end)
    elif level > self.levels.end:
      self.levels = IntRange(self.levels.start, level)

  def add_floor(self, floor: int):
    if len(self.floors) == 0:
      self.floors.append(IntRange(floor, floor))
    elif floor == self.floors[-1].end or floor == self.floors[-1].end + 1:
      self.floors[-1].end = floor
    else:
      self.floors.append(IntRange(floor, floor))

  def __lt__(self, other) -> bool:
    if self.floors[0].start != other.floors[0].start:
      return self.floors[0].start < other.floors[0].start
    return self.metadata.dex_number < other.metadata.dex_number

class ItemInfo:
  name: str
  floors: list[IntRange]

  def __init__(self, name: str):
    self.name = name
    self.floors = []

  def add_floors(self, floors: IntRange):
    if len(self.floors) == 0:
      self.floors.append(IntRange(floors.start, floors.end))
    elif floors.start == self.floors[-1].end + 1:
      self.floors[-1].end = floors.end
    else:
      self.floors.append(IntRange(floors.start, floors.end))

  def __lt__(self, other) -> bool:
    self_category = get_item_category(self.name)
    other_category = get_item_category(other.name)
    if self_category != other_category:
      return self_category.value < other_category.value
    return self.name.__lt__(other.name)

class ItemFloorRangeInfo:
  floor_range: IntRange
  raw_item_data: list[str]

  def __init__(self, floor_range: IntRange):
    self.floor_range = floor_range
    self.raw_item_data = []

  def __lt__(self, other) -> bool:
    return self.floor_range.start < other.floor_range.start

def get_floors_string(floors: list[IntRange]) -> str:
  return ', '.join([str(floor_range) for floor_range in floors])

def write_encountered_table():
  all_pokemon_info: dict[str, PokemonInfo] = {}
  wii_connect_pokemon = None
  wonder_mail_w_pokemon = None
  regigigas = False
  with open(POKEMON_FILE, 'r') as pokemon_file:
    current_floor = None
    boss = False

    for line in pokemon_file.readlines():
      if '\t' in line:
        line_split = line.split('\t')
        floor = line_split[0]
        pokemon = map_pokemon_name(line_split[1])
        level = int(line_split[2])

        if len(floor) > 0:
          boss = 'boss' in floor
          if boss:
            current_floor = int(floor[floor.rindex(' ') + 1 : -1])
          else:
            current_floor = int(floor[:-1])

        if pokemon not in all_pokemon_info:
          all_pokemon_info[pokemon] = PokemonInfo(pokemon)
        all_pokemon_info[pokemon].add_floor(current_floor)
        all_pokemon_info[pokemon].add_level(level)
        all_pokemon_info[pokemon].boss = boss
      elif 'Mystery Part' in line:
        pokemon = line.split(' ')[0]
        if pokemon in all_pokemon_info:
          all_pokemon_info[pokemon].mystery_part = True
        else:
          print(f'Could not find Pokémon {pokemon} to add Mystery Part to.')
      elif 'monthly' in line:
        wii_connect_pokemon = line.split(' ')[0]
      elif 'Regigigas' in line:
        regigigas = True
      elif 'RC24' in line:
        wonder_mail_w_pokemon = line.split(' ')[0]

  encountered_table = \
  f"""==Pokémon encountered==
{{{{mdloc/h|{type_style}}}}}
"""

  for pokemon_info in sorted(all_pokemon_info.values()):
    dex_number = pokemon_info.metadata.dex_number
    name = pokemon_info.name
    floors = get_floors_string(pokemon_info.floors)
    levels = pokemon_info.levels
    recruit_rate = pokemon_info.metadata.recruit_rate

    if pokemon_info.form:
      form = f'|{pokemon_info.form}'
    else:
      form = ''

    recruit_rate_string = f'{recruit_rate:.1f}'
    if pokemon_info.mystery_part:
      recruit_rate_string = f'{{{{tt|{recruit_rate_string}|Requires Mystery Part or Secret Slab and Slowking\'s Certification Rank}}}}'
    if not recruitable and not pokemon_info.boss:
      recruit_rate_string = '0'

    if pokemon_info.boss:
      boss = '|boss=yes'
    else:
      boss = ''

    if name == 'Unown':
      unown = '|unownrand=yes'
    else:
      unown = ''

    encountered_table += f'{{{{mdloc|{dex_number:03d}|{name}|{floors}|{levels}|{recruit_rate_string}{form}{boss}{unown}}}}}\n'

  footer_notes = []
  if wii_connect_pokemon is not None:
    footer_notes.append(f'{wii_connect_pokemon} only appears once per month with WiiConnect24.')
  if wonder_mail_w_pokemon is not None:
    footer_notes.append(f'{wonder_mail_w_pokemon} only appears with a challenge letter obtained via Wonder Mail W over Wi-Fi.')
  if regigigas:
    footer_notes.append('Regigigas appears if Regirock, Regice, and Registeel have been recruited.')

  if len(footer_notes) > 0:
    footer_text = f'|{'\n'.join(footer_notes)}'
  else:
    footer_text = ''

  encountered_table += f'{{{{mdloc/f|{type_style}{footer_text}}}}}\n\n'
  return encountered_table

def write_generic_item_table(all_item_info: dict[str, ItemInfo]):
  items_table = f"""
{{{{DungeonItem/h|{type_style}}}}}
"""

  for item_info in sorted(all_item_info.values()):
    name = item_info.name

    link = get_item_link(name)
    if link is None:
      link = ''
    else:
      link = f'|2={link}'

    floors = get_floors_string(item_info.floors)

    sprite = get_item_sprite(name)
    if sprite is None:
      sprite = ''
    else:
      sprite = f'|sprite={sprite}'

    if get_item_category(name) == ItemCategory.TM:
      f'{{{{DungeonItem/TM|{name}|{floors}}}}}'
    else:
      items_table += f'{{{{DungeonItem|{name}{link}|3={floors}{sprite}}}}}\n'

  items_table += '|}\n\n'
  return items_table

def write_items_table():
  all_item_info: dict[str, ItemInfo] = {}
  with open(ITEMS_FILE, 'r') as items_file:
    for line in items_file.readlines():
      if line.endswith('F\n'):
        start = line[:line.index('F')]
        if line.count('F') == 2:
          end = line[line.index('-') + 1 : line.rindex('F')]
        else:
          end = start
        floor_range = IntRange(int(start), int(end))

      elif '\t' in line:
        item_name = map_item_name(line.split('\t')[0])
        if item_name not in all_item_info:
          all_item_info[item_name] = ItemInfo(item_name)
        all_item_info[item_name].add_floors(floor_range)

  items_table = '==Items=='
  items_table += write_generic_item_table(all_item_info)
  return items_table

def write_subitem_table(file_name: str, header: str):
  split_item_lists: list[ItemFloorRangeInfo] = []
  all_item_info: dict[str, ItemInfo] = {}
  with open(file_name, 'r') as items_file:
    current_split_item_lists: list[ItemFloorRangeInfo] = []
    for line in items_file.readlines():
      if line.endswith('F\n'):
        current_split_item_lists.clear()
        floor_chances = line.split(', ')
        for floor_chance in floor_chances:
          if floor_chance.startswith('0%'):
            continue

          start_index = 0
          if 'floors' in floor_chance:
            start_index = floor_chance.index('floors ') + len('floors ')
          start = floor_chance[start_index : floor_chance.index('F')]
          if floor_chance.count('F') == 2:
            end = floor_chance[floor_chance.rindex('-') + 1 : floor_chance.rindex('F')]
          else:
            end = start
          floor_range = IntRange(int(start), int(end))
          item_floor_range_info = ItemFloorRangeInfo(floor_range)
          current_split_item_lists.append(item_floor_range_info)
          split_item_lists.append(item_floor_range_info)

      elif '\t' in line:
        for item_floor_range_info in current_split_item_lists:
          item_floor_range_info.raw_item_data.append(line)

  for split_item_list in sorted(split_item_lists):
    for line in split_item_list.raw_item_data:
      item_name = map_item_name(line.split('\t')[0])
      if item_name not in all_item_info:
        all_item_info[item_name] = ItemInfo(item_name)
      all_item_info[item_name].add_floors(split_item_list.floor_range)

  if len(all_item_info) == 0:
    return ''

  items_table = f'==={header}==='
  items_table += write_generic_item_table(all_item_info)
  return items_table

def write_monster_house_table():
  return ''

def write_footer():
  return \
  """{{-}}
{{PMD WiiWare locations}}
{{DoubleProjectTag|Locations|Sidegames}}

[[Category:Pokémon Mystery Dungeon (WiiWare) locations]]
[[Category:Dungeons containing Legendary or Mythical Pokémon]]"""

with open(DEST_FILE, 'w') as dest_file:
  dest_file.write(write_encountered_table())
  dest_file.write(write_items_table())
  dest_file.write(write_subitem_table(SHOP_FILE, 'Kecleon Shops'))
  dest_file.write(write_subitem_table(MONSTER_HOUSE_FILE, 'Monster Houses'))
  dest_file.write(write_footer())
