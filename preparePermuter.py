import os
import subprocess
from filePaths import PERMUTER_FOLDER
from permuterUtils import *

function_file = os.path.join('asm', 'permuter_function.c')
new_function = ''
with open(function_file, 'r') as file:
  for line in file.readlines():
    if '#include "global.h"' in line:
      continue

    mid_comment = line.find('/*')
    if mid_comment > -1:
      line = line[:mid_comment] + line[line.find('*/') + 3:]

    comment_index = line.find('//')
    if comment_index > -1:
      line = line[:comment_index] + '\n'
    new_function += line

new_function = """
typedef signed char int8_t;
typedef short int16_t;
typedef int int32_t;
typedef unsigned char uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int uint32_t;
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef int8_t s8;
typedef int16_t s16;
typedef int32_t s32;
typedef u8 bool8;
#define TRUE 1
#define FALSE 0
#define NULL ((void *)0)
""" + new_function

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