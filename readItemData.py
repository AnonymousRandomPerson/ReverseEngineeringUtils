from romUtils import read_offset_data
from data.itemData import item_map

read_offset_data(init_offset=0x30CC28, data_size=0x20, num_elements=0xEC, data_offset=0xC, read_size = 1, index_dict=item_map)
