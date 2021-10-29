import binascii, os
from dataclasses import dataclass, field
from io import BufferedReader
from typing import Dict, List
from data.itemData import item_map
from data.moveData import move_map
from data.speciesData import species_list

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

def read_u16(game_file: BufferedReader) -> int:
  return read_int(game_file, 2)

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

def get_species_macro(index: int) -> str:
  return 'SPECIES_' + strip_name(species_list[index].upper())

def get_move_macro(index: int) -> str:
  if index == 0:
    return None
  return 'MOVE_' + strip_name(move_map[index]).upper()

def get_item_macro(index: int) -> str:
  return 'ITEM_ID_' + strip_name(item_map[index]).upper()

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

  string_addresses[address] = StringDefinition(get_string_definition(constant_name, read_string(game_file, address), align), constant_name)
  return constant_name

def get_string_definition(constant_name: str, string: str, align=True):
  string = string.replace('¾', '♀').replace('½', '♂').replace('\n', '\\n')
  string += '\\0'
  string_data = ''
  is_string = None
  for char in string:
    char_ord = ord(char)
    # 0xE9 is é.
    current_is_string = char_ord < 0x7F or char_ord == 0xE9 or char == '♂' or char == '♀'

    if current_is_string:
      if is_string is not True:
        if is_string is not None:
          string_data += '\n'
        string_data += '.string "'
      string_data += char
    elif not current_is_string:
      if is_string is not False:
        if is_string is not None:
          string_data += '"\n'
        string_data += '.byte'
      else:
        string_data += ','
      string_data += ' 0x' + format(ord(char), '02x')

    is_string = current_is_string

  if is_string:
    string_data += '"'

  string_def = '.global %s\n' % constant_name
  string_def += '%s:\n' % constant_name
  string_def += string_data + '\n'
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
