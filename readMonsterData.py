from romUtils import read_offset_data
from data.monsterData import monster_map

read_offset_data(init_offset=0x357B98, data_size=72, num_elements=len(monster_map), data_offset=0x1B, read_size=1, index_dict=monster_map, decimal_values=True)
