from filePaths import *

import os

for root, _, files in os.walk(PRET_PMDSKY_FOLDER):
  for file in files:
    file_path = os.path.join(root, file)
    if file.endswith('.inc') and 'macros' not in file_path and 'syscall' not in file_path:
        with open(file_path, 'r') as include_file:
          asm_contents = include_file.read()

        asm_contents_split = asm_contents.split('\n')
        sorted_imports = sorted(asm_contents_split[1:], key=str.casefold)
        if len(sorted_imports) and sorted_imports[0] == '':
            sorted_imports = sorted_imports[1:]
        asm_contents = '#pragma once\n' + '\n'.join(sorted_imports) + '\n'

        with open(file_path, 'w') as include_file:
          include_file.write(asm_contents)