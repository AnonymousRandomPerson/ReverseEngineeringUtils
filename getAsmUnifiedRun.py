import os
from transformAsm import get_asm_unified

unified_file = os.path.join('asm', 'unified.txt')
with open(unified_file, 'w') as file:
  file.write(get_asm_unified())
