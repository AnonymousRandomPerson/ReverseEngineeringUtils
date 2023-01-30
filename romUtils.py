from typing import Dict, List
import binascii
from filePaths import GAME_FILE_PATH

def read_offset_data(init_offset: int, num_elements: int, data_size: int = 1, data_offset: int = 0, read_size: int = 1, index_dict: Dict[int, str] = None, include_unknown: bool = False, binary_values: bool = False, decimal_values: bool = False, mask: int = None, sorted_values = True, file_path = GAME_FILE_PATH, print_results = True):
  field_map: Dict[int, List] = {}

  with open(file_path, 'rb') as game_file:
    game_file.seek(init_offset + data_offset)

    for index in range(num_elements + 1):
      data = game_file.read(read_size)
      if binary_values or decimal_values or mask:
        field_value = int.from_bytes(data, 'little')
        if mask is not None:
          field_value &= mask
        if binary_values:
          field_value = format(field_value, '0%sb' % (read_size * 8))
        elif decimal_values:
          field_value = format(field_value, '0%sd' % read_size)
        else:
          field_value = format(field_value, '0%sx' % read_size)
      else:
        field_value = binascii.hexlify(bytearray(reversed(data)))

      index_name = None
      if index_dict is None or index not in index_dict and include_unknown:
        index_name = hex(index)
      elif index in index_dict:
        index_name = index_dict[index]

      if index_name is not None:
        if field_value not in field_map:
          field_map[field_value] = []
        field_map[field_value].append(index_name)

      game_file.seek(data_size - read_size, 1)

  field_keys = field_map.keys()
  if sorted_values:
    field_keys = sorted(field_keys)
  for field in field_keys:
    field_values = field_map[field]
    if sorted_values:
      field_values = list(sorted(field_values))
      field_map[field] = field_values
    if print_results:
      print('%s: %s' % (field, field_values))
  return field_map
