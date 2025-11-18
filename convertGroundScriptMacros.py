from filePaths import PRET_PMDRED_FOLDER
import os

ground_script_path = os.path.join(PRET_PMDRED_FOLDER, 'src', 'data', 'ground')

macro_name = 'CAMERA_END_PAN'
macro_opcode = '0x99'
used_args = []

map_values = {
  1: {
    0x0: 'SPECIAL_TEXT_UNK_0',
    0x1: 'SPECIAL_TEXT_UNK_1',
    0x2: 'SPECIAL_TEXT_WAITING',
    0x3: 'SPECIAL_TEXT_UNK_3',
    0x4: 'SPECIAL_TEXT_PLAYER_NAME_INPUT',
    0x5: 'SPECIAL_TEXT_TEAM_NAME_INPUT',
    0x6: 'SPECIAL_TEXT_PASSWORD_INPUT',
    0x7: 'SPECIAL_TEXT_FRIEND_MENU',
    0x8: 'SPECIAL_TEXT_MENU',
    0x9: 'SPECIAL_TEXT_YES_NO_WITH_LARGE_BOX',
    0xA: 'SPECIAL_TEXT_LARGE_TEXT_BOX',
    0xB: 'SPECIAL_TEXT_BUY_FRIEND_AREAS',
    0xC: 'SPECIAL_TEXT_DUNGEON_LIST',
    0xD: 'SPECIAL_TEXT_DOJO_LIST',
    0xE: 'SPECIAL_TEXT_SAVE_1',
    0xF: 'SPECIAL_TEXT_SAVE_2',
    0x10: 'SPECIAL_TEXT_STORAGE_WITH_DIALOG',
    0x11: 'SPECIAL_TEXT_STORAGE',
    0x12: 'SPECIAL_TEXT_UNK_12',
    0x13: 'SPECIAL_TEXT_BANK',
    0x14: 'SPECIAL_TEXT_UNK_14',
    0x15: 'SPECIAL_TEXT_UNK_15',
    0x16: 'SPECIAL_TEXT_FRIEND_AREA_SELECT',
    0x17: 'SPECIAL_TEXT_GREEN_KECLEON_SHOP',
    0x18: 'SPECIAL_TEXT_PURPLE_KECLEON_SHOP',
    0x19: 'SPECIAL_TEXT_LINK_SHOP',
    0x1A: 'SPECIAL_TEXT_LUMINOUS_CAVE',
    0x1B: 'SPECIAL_TEXT_FRIEND_SHOP',
    0x1C: 'SPECIAL_TEXT_FRIEND_RESCUE',
    0x1D: 'SPECIAL_TEXT_UNK_1D',
    0x1E: 'SPECIAL_TEXT_THANK_YOU_MAIL',
    0x1F: 'SPECIAL_TEXT_PPO_HELP_COUNTER',
    0x20: 'SPECIAL_TEXT_BULLETIN_BOARD_JOBS',
    0x21: 'SPECIAL_TEXT_BULLETIN_BOARD',
    0x22: 'SPECIAL_TEXT_UNK_22',
    0x23: 'SPECIAL_TEXT_UNK_23',
    0x24: 'SPECIAL_TEXT_DOJO_ENTER',
    0x25: 'SPECIAL_TEXT_DOJO_SUCCESS',
    0x26: 'SPECIAL_TEXT_DOJO_FAILURE',
    0x27: 'SPECIAL_TEXT_DOJO_ALL_CLEARED',
    0x28: 'SPECIAL_TEXT_PERSONALITY_QUIZ',
    0x29: 'SPECIAL_TEXT_UNK_29',
    0x2A: 'SPECIAL_TEXT_SCRIPTING_MENU',
    0x2B: 'SPECIAL_TEXT_ITEM_REWARD',
    0x2C: 'SPECIAL_TEXT_UNK_2C',
    0x2D: 'SPECIAL_TEXT_TOOL_BOX',
    0x2E: 'SPECIAL_TEXT_CREDITS_NAME',
  }
}
# map_values = {
#   3: {
#     0: 'DIRECTION_SOUTH',
#     1: 'DIRECTION_SOUTHEAST',
#     2: 'DIRECTION_EAST',
#     3: 'DIRECTION_NORTHEAST',
#     4: 'DIRECTION_NORTH',
#     5: 'DIRECTION_NORTHWEST',
#     6: 'DIRECTION_WEST',
#     7: 'DIRECTION_SOUTHWEST',
#   }
# }

for root, _, files in os.walk(ground_script_path):
  for file in files:
    file_path = os.path.join(root, file)
    if file.endswith('.h'):
      with open(file_path, 'r') as script_file:
        contents = script_file.readlines()

      changed = False
      for i, line in enumerate(contents):
        if line.startswith(f'    {{ ' + macro_opcode):
          split_line = line.split(',')
          print(line, file)
          line = f'    {macro_name}'

          if len(used_args) > 0:
            decimal_args = []
            for arg in used_args:
              decimal_arg = int(split_line[arg].lstrip(), 16)
              if arg in map_values:
                decimal_arg = map_values[arg][decimal_arg]
              decimal_args.append(str(decimal_arg))
            line += f'({str.join(', ', decimal_args)})'

          contents[i] = line + ',\n'
          changed = True

      if changed:
        with open(file_path, 'w') as script_file:
          script_file.writelines(contents)
