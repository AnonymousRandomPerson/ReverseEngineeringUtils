from romUtils import read_offset_data
from data.speciesData import species_map

read_offset_data(init_offset=0x357B98, data_size=72, num_elements=len(species_map), data_offset=0x1B, read_size=1, index_dict=species_map, decimal_values=True)
