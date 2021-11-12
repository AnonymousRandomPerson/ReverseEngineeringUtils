import os

def get_function_name():
  raw_asm_file = os.path.join('asm', 'raw.txt')
  with open(raw_asm_file, 'r') as file:
    file.readline()
    second_line = file.readline()
    return second_line[:-2]
