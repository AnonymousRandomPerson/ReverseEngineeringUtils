from filePaths import *
import os

disasm_output_path = os.path.join(NDSDISASM_FOLDER, 'output', 'jp')
disasm_configs_path = os.path.join(NDSDISASM_FOLDER, 'config', 'jp')

overlay = '34'
if overlay.startswith('arm') or overlay == 'itcm':
  overlay_prefix = 'sub'
else:
  overlay_prefix = f'ov{overlay}'
disasm_overlay_path = os.path.join(disasm_output_path, f'pmdsky_{overlay}.s')
disasm_config_path = os.path.join(disasm_configs_path, f'pmdsky_{overlay}.cfg')

with open(disasm_overlay_path, 'r') as disasm_overlay_file:
  disasm_overlay_lines = disasm_overlay_file.readlines()

config_addresses = set()
with open(disasm_config_path) as disasm_config_file:
  for line in disasm_config_file.readlines():
    config_addresses.add(line.split(' ')[1][2:].upper())

holes = []
current_start_hole = None
for i, line in enumerate(disasm_overlay_lines[:-1]):
  if line.startswith('\t.data'):
    break
  if line.startswith('\t.byte'):
    if current_start_hole is None:
      current_start_hole = i
      hole_address = disasm_overlay_lines[current_start_hole - 1][1:-2]
      if hole_address not in config_addresses:
        print(f'arm_func 0x{hole_address} {overlay_prefix}_{hole_address}')
  elif current_start_hole is not None:
    current_start_hole = None
