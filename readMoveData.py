from romUtils import read_offset_data
from data.moveData import move_map, move_map_sky
from filePaths import WAZA_FILE_PATH

# read_offset_data(init_offset=0x3679a0, data_size=36, num_elements=len(move_map), data_offset=0xA, read_size=2, index_dict=move_map, binary_values=True, decimal_values=False, mask=0xF0)

ai_targets = read_offset_data(init_offset=0xE0E0, data_size=26, num_elements=543, data_offset=0x6, read_size=2, index_dict=move_map_sky, binary_values=True, mask=0xF0, file_path=WAZA_FILE_PATH)