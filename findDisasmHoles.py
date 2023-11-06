from filePaths import *
import os

disasm_output_path = os.path.join(NDSDISASM_FOLDER, 'output')
disasm_configs_path = os.path.join(NDSDISASM_FOLDER, 'config')
decomp_asm_path = os.path.join(PRET_PMDSKY_FOLDER, 'asm')

overlay = 'arm7'
if overlay == 'arm7':
  overlay_file_name = f'{overlay}.s'
  decomp_asm_path = os.path.join(PRET_PMDSKY_FOLDER, 'sub', 'asm')
else:
  overlay_file_name = f'overlay_{overlay}.s'
overlay_path = os.path.join(decomp_asm_path, overlay_file_name)
disasm_overlay_path = os.path.join(disasm_output_path, f'pmdsky_{overlay}.s')
disasm_config_path = os.path.join(disasm_configs_path, f'pmdsky_{overlay}.cfg')

with open(overlay_path, 'r') as overlay_file:
  overlay_lines = overlay_file.readlines()

holes = []
current_start_hole = None
for i, line in enumerate(overlay_lines[:-1]):
  if line.startswith('\t.data'):
    break
  if line.startswith('\t.byte'):
    if current_start_hole is None:
      current_start_hole = i
  elif current_start_hole is not None:
    holes.append((current_start_hole, i))
    current_start_hole = None

hole_addresses = []

for start_hole, end_hole in holes:
  hole_address = overlay_lines[start_hole - 1][1:-2]
  hole_addresses.append(hole_address)

for i, line in enumerate(overlay_lines):
  for hole_address in hole_addresses:
    overlay_lines[i] = line.replace(f'0x{hole_address}', f'ov{overlay}_{hole_address}')

disasm_function_start_lines = {}
with open(disasm_overlay_path) as disasm_overlay_file:
  disasm_overlay_lines = disasm_overlay_file.readlines()

config_addresses = set()
with open(disasm_config_path) as disasm_config_file:
  for line in disasm_config_file.readlines():
    config_addresses.add(line.split(' ')[1][2:].upper())

if overlay == 'arm7':
  overlay_prefix = 'sub'
else:
  overlay_prefix = f'ov{overlay}'
for i, line in enumerate(disasm_overlay_lines):
  if line.startswith('\tarm_func_start'):
    offset = len('\tarm_func_start ')
    function_name = line[offset:-1].replace('FUN', overlay_prefix)
    disasm_function_start_lines[function_name] = i

new_lines = []
new_lines_progress = 0
for start_hole, end_hole in holes:
  hole_address = overlay_lines[start_hole - 1][1:-2]
  end_hole_line = overlay_lines[end_hole + 2]
  if ':' in end_hole_line:
    start_hole_function_name = f'{overlay_prefix}_{hole_address}'
    end_hole_function_name = end_hole_line[:end_hole_line.find(':')]
    if start_hole_function_name in disasm_function_start_lines and end_hole_function_name in disasm_function_start_lines:
      new_lines.extend(overlay_lines[new_lines_progress:start_hole - 1])
      new_lines.extend(disasm_overlay_lines[disasm_function_start_lines[start_hole_function_name] - 1 : disasm_function_start_lines[end_hole_function_name]])
      new_lines_progress = end_hole + 1
    elif hole_address in config_addresses:
      print(f'Failed to fill in function at address {hole_address}')
    else:
      print(f'arm_func 0x{hole_address} {overlay_prefix}_{hole_address}')
  else:
    print(f'Unknown hole end at lines', start_hole, end_hole)

new_lines.extend(overlay_lines[new_lines_progress:])

with open(overlay_path, 'w') as overlay_file:
  overlay_file.writelines(new_lines)
