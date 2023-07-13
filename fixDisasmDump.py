from filePaths import *
from textUtils import *
import os

disasm_config_path = os.path.join(PRET_FOLDER, 'ndsdisasm', 'config')
decomp_asm_path = os.path.join(PRET_PMDSKY_FOLDER, 'asm')

mapped_function_names = {}

overlay_files = ['main', 'itcm']
config_file_names = ['arm9', 'itcm']
for i in range(0, 35):
  config_file_names.append(f'{i:02}')
  overlay_files.append(f'{i:02}')

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
          mapped_function_names[function_address] = function_name

def convert_search_mnemonic(search):
  return f'\t{search} '

arm_start_replacements = [
  ('ldm', 'ldmia'),
  ('push', 'stmdb sp!,'),
  ('pop', 'ldmdb sp!,'),
  ('stm', 'stmia'),
]

thumb_start_replacements = [
  ('adcs', 'adc'),
  ('adds', 'add'),
  ('ands', 'and'),
  ('asrs', 'asr'),
  ('bics', 'bic'),
  ('eors', 'eor'),
  ('ldm', 'ldmia'),
  ('lsls', 'lsl'),
  ('lsrs', 'lsr'),
  ('mvns', 'mvn'),
  ('orrs', 'orr'),
  ('stm', 'stmia'),
  ('subs', 'sub'),
]

condition_codes = ['eq', 'ge', 'gt', 'hi', 'hs', 'le', 'lo', 'ls', 'lt', 'mi', 'ne', 'pl']
shift_suffixes = ['', 's']

for condition_code in condition_codes:
  shift_suffixes.append(condition_code)
  arm_start_replacements.append((f'ands{condition_code}', f'and{condition_code}s'))
  arm_start_replacements.append((f'ldm{condition_code}', f'ldm{condition_code}ia'))
  arm_start_replacements.append((f'ldrb{condition_code}', f'ldr{condition_code}b'))
  arm_start_replacements.append((f'ldrh{condition_code}', f'ldr{condition_code}h'))
  arm_start_replacements.append((f'ldrsb{condition_code}', f'ldr{condition_code}sb'))
  arm_start_replacements.append((f'ldrsh{condition_code}', f'ldr{condition_code}sh'))
  arm_start_replacements.append((f'pop{condition_code}', f'ldm{condition_code}db sp!,'))
  arm_start_replacements.append((f'stm{condition_code}', f'stm{condition_code}ia'))
  arm_start_replacements.append((f'strb{condition_code}', f'str{condition_code}b'))
  arm_start_replacements.append((f'strh{condition_code}', f'str{condition_code}h'))
  arm_start_replacements.append((f'stmib{condition_code}', f'stm{condition_code}ib'))
  arm_start_replacements.append((f'subs{condition_code}', f'sub{condition_code}s'))

for start_replacements in [arm_start_replacements, thumb_start_replacements]:
  for i in range(len(start_replacements)):
    start_replacements[i] = (convert_search_mnemonic(start_replacements[i][0]), convert_search_mnemonic(start_replacements[i][1]))

thumb_start_replacements.append(('\tsvc #', '\tswi '))
arm_start_replacements.append(('\tsvc #', '\tswi '))

shift_replacements = ['lsr', 'lsl', 'asr', 'ror']

overlay_files = ['main']
for overlay_file in overlay_files:
  missing_functions = set()
  if overlay_file == 'main' or overlay_file == 'itcm':
    overlay_file += '.s'
  else:
    overlay_file = f'overlay_{overlay_file}.s'

  overlay_path = os.path.join(decomp_asm_path, overlay_file)
  if not os.path.exists(overlay_path):
    continue
  with open(overlay_path, 'r') as overlay_file:
    new_lines = []
    arm_function = True
    for line in overlay_file.readlines():
      if line.startswith('\tarm_func_start'):
        arm_function = True
      elif line.startswith('\tthumb_func_start'):
        arm_function = False

      line = line.replace('@', ';', 1)
      line = line.replace('.4byte', '.word', 1)
      line = line.replace('.2byte', '.hword', 1)

      found_instruction = False

      if arm_function:
        start_replacements = arm_start_replacements
      else:
        start_replacements = thumb_start_replacements

      for start_replacement in start_replacements:
        search, replace = start_replacement
        if line.startswith(search):
          line = replace + line[len(search):]
          found_instruction = True
          break

      if not found_instruction:
        if line.startswith(convert_search_mnemonic('rrxs')):
          line = line.replace('rrxs', 'movs')[:-1] + ', rrx\n'
        elif line.startswith(convert_search_mnemonic('rrx')):
          line = line.replace('rrx', 'mov')[:-1] + ', rrx\n'

        elif line.startswith('\tmcr') or line.startswith('\tmrc'):
          line = line.replace('#', '')

        elif line.startswith('\tmrs') or line.startswith('\tmsr'):
          line = line.replace('apsr', 'cpsr').replace('nzcvq', 'f')

      if not found_instruction:
        if arm_function:
          for shift_replacement in shift_replacements:
            for condition_code in shift_suffixes:
              if line.startswith(convert_search_mnemonic(shift_replacement + condition_code)):
                line = line.replace(shift_replacement, 'mov', 1)
                last_argument = line.rfind(',') + 1
                line = line[:last_argument] + f' {shift_replacement}' + line[last_argument:]
                found_instruction = True
                break
            if found_instruction:
              break
        else:
          if line.startswith(convert_search_mnemonic('movs')):
            if '#' in line or line.count(',') == 1:
              line = line.replace('movs', 'mov', 1)
            found_instruction = True
          
          elif line.startswith(convert_search_mnemonic('muls')):
            line = line.replace('muls', 'mul', 1)
            line = line[:line.rfind(',')] + '\n'
            found_instruction = True

          elif line.startswith(convert_search_mnemonic('rsbs')):
            line = line.replace('rsbs', 'neg', 1)
            line = line[:line.rfind(',')] + '\n'
            found_instruction = True

      find_index = line.find('FUN_')
      if find_index >= 0:
        start_offset = len('FUN_')
        function_address_start = find_index + start_offset
        function_address_end = find_index + start_offset + 8
        function_address = line[find_index + start_offset : find_index + start_offset + 8]
        if function_address in mapped_function_names:
          line = line[:find_index] + mapped_function_names[function_address] + line[function_address_end:]
        else:
          missing_functions.add(function_address)
      new_lines.append(line)

  with open(overlay_path, 'w') as overlay_file:
    overlay_file.writelines(new_lines)

  # for function in sorted(missing_functions):
  #   print(function)