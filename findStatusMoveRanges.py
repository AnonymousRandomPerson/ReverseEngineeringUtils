from romUtils import read_offset_data
from data.moveData import move_map, move_map_sky
from filePaths import WAZA_FILE_PATH

ai_targets = read_offset_data(init_offset=0xE0E0, data_size=26, num_elements=543, data_offset=0x6, read_size=2, index_dict=move_map_sky, binary_values=True, mask=0xF0, file_path=WAZA_FILE_PATH, print_results=False)

move_targets = read_offset_data(init_offset=0xE0E0, data_size=26, num_elements=543, data_offset=0x4, read_size=2, index_dict=move_map_sky, binary_values=True, mask=0xF0, file_path=WAZA_FILE_PATH, print_results=False)

categories = read_offset_data(init_offset=0xE0E0, data_size=26, num_elements=543, data_offset=0x3, read_size=1, index_dict=move_map_sky, file_path=WAZA_FILE_PATH, print_results=False)

range_types = read_offset_data(init_offset=0xE0E0, data_size=26, num_elements=543, data_offset=0x15, read_size=1, index_dict=move_map_sky, file_path=WAZA_FILE_PATH, print_results=False)

allowed_moves = set(categories[b'02']) & set(move_targets['0000000001110000'])


# ai_targets = read_offset_data(init_offset=0x3679a0, data_size=36, num_elements=len(move_map), data_offset=0xA, read_size=2, index_dict=move_map, binary_values=True, mask=0xF0, print_results=False)

# move_targets = read_offset_data(init_offset=0x3679a0, data_size=36, num_elements=len(move_map), data_offset=0x8, read_size=2, index_dict=move_map, binary_values=True, mask=0xF0, print_results=False)

# range_types = read_offset_data(init_offset=0x3679a0, data_size=36, num_elements=len(move_map), data_offset=0x19, read_size=1, index_dict=move_map, print_results=False)

# allowed_moves = set(move_targets['0000000001110000']) & set(range_types[b'13'])

one_tile_moves = [move for move in ai_targets['0000000000000000'] if move in allowed_moves]
two_tile_moves = [move for move in ai_targets['0000000001000000'] if move in allowed_moves]
room_moves = [move for move in ai_targets['0000000000110000'] if move in allowed_moves]

print('One-tile:', sorted(one_tile_moves))
print('Two-tile:', sorted(two_tile_moves))
print('Room:', sorted(room_moves))

# for moves in ai_targets.values():
#   pass
