import os
import re
from dataclasses import dataclass
from filePaths import PERMUTER_FOLDER
from permuterUtils import *

@dataclass
class ReplaceText:
  find: str
  replace: str

output_folder = 'output-1180-1'
replace_strings = [
  ReplaceText('0x80', 'GROUND_ITEM_TOOLBOX_INDEX'),
  ReplaceText('0x81', 'HELD_ITEM_TOOLBOX_INDEX'),
  ReplaceText('useHeldItem = 0', 'useHeldItem = FALSE'),
  ReplaceText('itemType == 0', 'itemType == ITEM_TYPE_THROWABLE'),
  ReplaceText('itemType == 1', 'itemType == ITEM_TYPE_ROCK'),
  ReplaceText('potentialTargetPositions, 1)', 'potentialTargetPositions, TRUE)'),
  ReplaceText('potentialTargetPositions, 0)', 'potentialTargetPositions, FALSE)'),
  ReplaceText('item, 2)', 'item, TARGET_ALLY)'),
  ReplaceText('item, 0)', 'item, FALSE)'),
  ReplaceText('itemType == 9', 'itemType == ITEM_TYPE_ORB'),
]

output_function_file = os.path.join(PERMUTER_FOLDER, 'nonmatchings', output_folder, 'source.c')

with open(output_function_file, 'r') as file:
  code = file.read()

function_name = get_function_name()
function_index = code.find(function_name + '(')
if function_index < 0:
  raise Exception('Failed to find function %s' % function_name)
function_start_index = code.rfind('\n', 0, function_index)
code = code[function_start_index + 1:]

code = code.replace('  ', '    ').replace('(void *) 0', 'NULL')
code = re.sub('else\n +if', 'else if', code)
code = re.sub('\n{2,}', '\n', code)

for replace_string in replace_strings:
  code = code.replace(replace_string.find, replace_string.replace)

cleaned_function_file = os.path.join('asm', 'cleaned_function.c')
with open(cleaned_function_file, 'w') as file:
  file.write(code)
