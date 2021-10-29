from romUtils import read_offset_data
from data.moveData import move_map

read_offset_data(init_offset=0x3679a0, data_size=36, num_elements=len(move_map), data_offset=0x8, read_size=1, index_dict=move_map, binary_values=False, decimal_values=True, mask=None)
