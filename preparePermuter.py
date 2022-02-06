import os
import subprocess
from filePaths import PERMUTER_FOLDER
from permuterUtils import *

function_file = os.path.join('asm', 'permuter_function.c')
new_function = ''
with open(function_file, 'r') as file:
  for line in file.readlines():
    mid_comment = line.find('/*')
    if mid_comment > -1:
      line = line[:mid_comment] + line[line.find('*/') + 3:]

    comment_index = line.find('//')
    if comment_index > -1:
      line = line[:comment_index] + '\n'
    new_function += line

transformed_asm_file = os.path.join('asm', 'transformed.txt')

function_name = get_function_name()

with open(transformed_asm_file, 'r') as file:
  asm = file.read()
asm = """
.syntax unified
.thumb

""" + function_name + ':\n' + asm

base_file = os.path.join(PERMUTER_FOLDER, 'nonmatchings', 'base.c')
with open(base_file, 'w') as file:
  file.write(new_function)

target_file = os.path.join(PERMUTER_FOLDER, 'nonmatchings', 'target.s')
with open(target_file, 'w') as file:
  file.write(asm)

def runCommand(command: str):
  subprocess.Popen(command.split(), cwd=os.path.join(PERMUTER_FOLDER, 'nonmatchings'))

runCommand('./compile.sh base.c -o base.o')
runCommand('arm-none-eabi-as -mthumb -mthumb-interwork -mcpu=arm7tdmi target.s -o target.o')