from romUtils import read_offset_data
from data.moveData import move_map

read_offset_data(init_offset=0x53e94, data_size=4, num_elements=411, read_size=4, index_dict=move_map)
