from romUtils import read_offset_data
from data.itemData import item_map

read_offset_data(init_offset=0x48f58, data_size=4, num_elements=(0x4928c - 0x48f58) // 4, read_size=4, index_dict=item_map)
