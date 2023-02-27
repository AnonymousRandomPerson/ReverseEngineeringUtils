import binascii, os
from dataclasses import dataclass, field
from io import BufferedReader
from typing import Dict, List, Set
from data.itemData import item_map
from data.moveData import move_map
from data.monsterData import monster_list

@dataclass
class JsonStringField:
  field: str
  prefix: str
  replace_names: Dict[str, str] = field(default_factory=dict)
  skip_names: Dict[str, str] = field(default_factory=dict)

@dataclass
class StringDefinition:
  definition: str
  constant_name: str

@dataclass
class SpecialCharDefinition:
  sequence: List[str]
  keyword: str

def get_current_address(game_file: BufferedReader) -> str:
  return '0x' + format(game_file.tell() + 0x08000000, '08x')

def read_pointer(game_file: BufferedReader) -> str:
  return '0x' + binascii.hexlify(bytearray(reversed(game_file.read(4)))).decode('utf-8')

def read_int(game_file: BufferedReader, num_bytes: int) -> int:
  return int.from_bytes(game_file.read(num_bytes), 'little')

def read_binary(game_file: BufferedReader, num_bytes: int) -> str:
  return '0b' + format(read_int(game_file, num_bytes), '0%sb' % (num_bytes * 8))

def read_bool8(game_file: BufferedReader) -> int:
  return read_int(game_file, 1) != 0

def read_u8(game_file: BufferedReader) -> int:
  return read_int(game_file, 1)

def read_s8(game_file: BufferedReader) -> int:
  value = read_int(game_file, 1)
  if value > 127:
    value -= 256
  return value

def read_u16(game_file: BufferedReader) -> int:
  return read_int(game_file, 2)

def read_s16(game_file: BufferedReader) -> int:
  value = read_int(game_file, 2)
  if value > 32767:
    value -= 65536
  return value

def read_s32(game_file: BufferedReader) -> int:
  return read_int(game_file, 4)

def read_binary16(game_file: BufferedReader) -> str:
  return read_binary(game_file, 2)

def read_array(array_size: int, read_func) -> List:
  array = []
  for _ in range(array_size):
    array.append(read_func(None))
  return array

def read_bool8_array(game_file: BufferedReader, array_size: int) -> List[int]:
  return read_array(array_size, lambda _: read_bool8(game_file))

def read_u8_array(game_file: BufferedReader, array_size: int) -> List[int]:
  return read_array(array_size, lambda _: read_int(game_file, 1))

def read_u16_array(game_file: BufferedReader, array_size: int) -> List[int]:
  return read_array(array_size, lambda _: read_int(game_file, 2))

def read_string(game_file: BufferedReader, address: str) -> str:
  game_file.seek(int(address[4:], 16))
  address_string = ''
  current_char = None
  while True:
    current_char = int.from_bytes(game_file.read(1), 'little')
    if current_char == 0:
      break
    address_string += chr(current_char)

  return address_string

def strip_name(name: str, use_underscores=True) -> str:
  if use_underscores:
    space = '_'
  else:
    space = ''
  return name.replace(' ', space).replace('-', space).replace('♀', '_F').replace('♂', '_M').replace('.', '').replace('!', 'EMark').replace('?', 'QMark').replace("'", '').replace('\u00e9', 'e')

def get_monster_macro(index: int) -> str:
  return 'MONSTER_' + strip_name(monster_list[index].upper())

def get_move_macro(index: int) -> str:
  if index == 0:
    return None
  return 'MOVE_' + strip_name(move_map[index]).upper()

def get_item_macro(index: int) -> str:
  return 'ITEM_' + strip_name(item_map[index]).upper()

def assign_nondefault(json_data: Dict, key: str, value):
  if isinstance(value, list):
    if any(value):
      json_data[key] = value
  elif isinstance(value, str):
    if value and (not value.startswith('0b') or '1' in value[2:]):
      json_data[key] = value
  elif value:
    json_data[key] = value

def add_string_definition(game_file: BufferedReader, string_addresses: Dict[str, StringDefinition], address: str, constant_name: str, align=True):
  if address in string_addresses:
    existing_constant = string_addresses[address].constant_name
    # print('Found duplicate constant for %s: %s.' % (constant_name, existing_constant))
    return existing_constant

  string_addresses[address] = StringDefinition(StringDefinitionBuilder().get_string_definition(constant_name, read_string(game_file, address), align), constant_name)
  return constant_name

def sequence_ord(text: str):
  return [ord(c) for c in text]

class StringDefinitionBuilder:

  special_char_sequences: Dict[str, SpecialCharDefinition] = {}
  accepted_special_chars: Set[str] = set()

  def initialize_special_char_sequences():
    special_char_definitions = [
      SpecialCharDefinition([0x81, 0x48], '？'),
      SpecialCharDefinition([0x82, 0xA4], 'う'),
      SpecialCharDefinition([0x82, 0xAA], 'か'),
      SpecialCharDefinition([0x82, 0xB7], 'す'),
      SpecialCharDefinition([0x82, 0xC8], 'な'),
      SpecialCharDefinition([0x82, 0xC9], 'に'),
      SpecialCharDefinition([0x82, 0xCC], 'も'),
      SpecialCharDefinition([0x82, 0xDC], 'み'),
      SpecialCharDefinition([0x82, 0xDD], 'ま'),
      SpecialCharDefinition([0x82, 0xE0], 'の'),
      SpecialCharDefinition([0x82, 0xE6], 'よ'),
      SpecialCharDefinition([0x82, 0xE9], 'る'),
      SpecialCharDefinition([0x82, 0xF0], 'を'),
      SpecialCharDefinition([0x82, 0xF1], 'ん'),
      SpecialCharDefinition([0x83, 0xBF, 0x83, 0xC4], 'POKE'),
      SpecialCharDefinition([0x87, 0x4E], 'TM'),
      SpecialCharDefinition([0x87, 0x4F], 'ORB'),
      SpecialCharDefinition(sequence_ord('#CD'), 'COLOR_1 YELLOW_4'),
      SpecialCharDefinition(sequence_ord('#CN'), 'COLOR_1 YELLOW_5'),
      SpecialCharDefinition(sequence_ord('#c4'), 'COLOR_2 GREEN'),
      SpecialCharDefinition(sequence_ord('#c5'), 'COLOR_2 CYAN'),
      SpecialCharDefinition(sequence_ord('#c6'), 'COLOR_2 YELLOW'),
      SpecialCharDefinition(sequence_ord('#R'), 'END_COLOR_TEXT_1'),
      SpecialCharDefinition(sequence_ord('#r'), 'END_COLOR_TEXT_2'),
      SpecialCharDefinition(sequence_ord('#n'), 'NEW_LINE'),
      SpecialCharDefinition(sequence_ord('~27'), 'APOSTROPHE'),
      SpecialCharDefinition(sequence_ord('~2c'), 'COMMA'),
      SpecialCharDefinition(sequence_ord('~93'), 'QUOTE_START'),
      SpecialCharDefinition(sequence_ord('~94'), 'QUOTE_END'),
      SpecialCharDefinition(sequence_ord('$m0'), 'ARG_POKEMON_0'),
      SpecialCharDefinition(sequence_ord('$i0'), 'ARG_MOVE_ITEM_0'),
    ]
    for definition in special_char_definitions:
      first_char = definition.sequence[0]
      if first_char not in StringDefinitionBuilder.special_char_sequences:
        StringDefinitionBuilder.special_char_sequences[first_char] = []
      StringDefinitionBuilder.special_char_sequences[first_char].append(definition)
      if len(definition.keyword) == 1:
        StringDefinitionBuilder.accepted_special_chars.add(definition.keyword)

  def append_char(self, char: str):
    if len(char) == 1:
      char_ord = ord(char)
      # 0xE9 is é.
      self.current_is_string = char_ord < 0x7F or char_ord == 0xE9 or char == '♂' or char == '♀' or char in StringDefinitionBuilder.accepted_special_chars
    else:
      self.current_is_string = True

    if self.current_is_string:
      if self.is_string is not True:
        if self.is_string is not None:
          self.string_data += '\n'
        self.string_data += '.string "'
      self.string_data += char
    elif not self.current_is_string:
      if self.is_string is not False:
        if self.is_string is not None:
          self.string_data += '"\n'
        self.string_data += '.byte'
      else:
        self.string_data += ','
      self.string_data += ' 0x' + format(ord(char), '02x')

    self.is_string = self.current_is_string

  def get_string_definition(self, constant_name: str, string: str, align=True):
    if len(StringDefinitionBuilder.special_char_sequences) == 0:
      StringDefinitionBuilder.initialize_special_char_sequences()

    string = string.replace('¾', '♀').replace('½', '♂').replace('\n', '\\n')
    string += '\\0'
    self.string_data = ''
    self.is_string = None
    special_chars: List[str] = None
    for char in string:
      char_ord = ord(char)
      if special_chars is not None:
        special_chars.append(char_ord)

        continue_special_char = False
        matching_definition = None
        for definition in StringDefinitionBuilder.special_char_sequences[special_chars[0]]:
          if len(definition.sequence) < len(special_chars):
            continue
          match = True
          for i in range(1, len(special_chars)):
            if special_chars[i] != definition.sequence[i]:
              match = False
              break
          if match:
            if len(definition.sequence) > len(special_chars):
              continue_special_char = True
            else:
              matching_definition = definition
            break

        if continue_special_char:
          continue
        elif matching_definition is not None:
          keyword = matching_definition.keyword
          if len(keyword) > 1:
            keyword = '{%s}' % keyword
          self.append_char(keyword)
          special_chars = None
          continue
        else:
          for special_char in special_chars[:-1]:
            self.append_char(chr(special_char))
          special_chars = None
      elif char_ord in StringDefinitionBuilder.special_char_sequences:
        special_chars = [char_ord]
        continue

      self.append_char(char)

    if self.is_string:
      self.string_data += '"'

    string_def = '.global %s\n' % constant_name
    string_def += '%s:\n' % constant_name
    string_def += self.string_data + '\n'
    if align:
      string_def += '.align 2,0\n'
    return string_def

def generate_string_file(game_file: BufferedReader, json_array: List[Dict], file_name: str, json_fields: List[JsonStringField], align=True):
  string_addresses: Dict[str, StringDefinition] = {}
  for json_item in json_array:
    stripped_name = strip_name(json_item['name'], use_underscores=False)
    for json_field in json_fields:
      name = stripped_name
      if name in json_field.skip_names:
        json_item[json_field.field] = json_field.skip_names[name]
      else:
        if name in json_field.replace_names:
          name = json_field.replace_names[name]
        json_item[json_field.field] = add_string_definition(game_file, string_addresses, json_item[json_field.field], json_field.prefix + name, align)

  combined_string = ''
  for address in sorted(string_addresses.keys()):
    combined_string = combined_string + '\n' + string_addresses[address].definition

  with open(os.path.join('json', file_name), 'w') as string_file:
    string_file.write(combined_string[1:])
