from filePaths import *
import os

disasm_config_path = os.path.join(PRET_FOLDER, 'ndsdisasm', 'config')

config_file_names = ['arm9']
for i in range(0, 35):
  config_file_names.append(f'{i:02}')

for config_file_name in config_file_names:
  config_path = os.path.join(disasm_config_path, f'pmdsky_{config_file_name}.cfg')
  if not os.path.exists(config_path):
    continue

  with open(config_path, 'r') as config_file:
    new_lines = []
    for line in config_file.readlines():
      line_split = line.replace('\n', '').split(' ')
      function_name = line_split[2]
      if function_name.startswith(f'ov{config_file_name}_') or function_name.startswith('sub_'):
        function_name_address = function_name[function_name.find('_') + 1:]
        function_address = line_split[1][2:].upper()
        if function_name_address != function_address:
          line = line.replace(function_name_address, function_address)
      new_lines.append(line)
  
  with open(config_path, 'w') as config_file:
    config_file.writelines(new_lines)
  