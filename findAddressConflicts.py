from filePaths import *
import os

disasm_config_path = os.path.join(PRET_FOLDER, 'ndsdisasm', 'config')

mapped_function_names = {}
config_file_names = ['arm9', 'itcm']

for i in range(0, 35):
  config_file_names.append(f'{i:02}')

for config_file_name in config_file_names:
  config_path = os.path.join(disasm_config_path, f'pmdsky_{config_file_name}.cfg')
  if os.path.exists(config_path):
    with open(config_path, 'r') as config_file:
      for line in config_file.readlines():
        if line.startswith('thumb'):
          start_offset = len('thumb_func 0x')
        else:
          start_offset = len('arm_func 0x')
        function_address = line[start_offset : start_offset + 8].upper()
        function_name = line[start_offset + 9 : -1]
        if function_address not in mapped_function_names:
          mapped_function_names[function_address] = (config_file_name, function_name)
        else:
          print(function_address, config_file_name, mapped_function_names[function_address])