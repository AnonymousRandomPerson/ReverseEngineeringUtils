from romUtils import read_offset_data
from data.moveData import move_map

offset_move_map = {moveId - 3: move for moveId, move in move_map.items() if moveId >= 3}

read_offset_data(init_offset=0x5cf00, data_size=4, num_elements=379, read_size=4, index_dict=offset_move_map)
