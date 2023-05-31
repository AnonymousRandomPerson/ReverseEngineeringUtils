import os, struct
from filePaths import *
from dataclasses import dataclass
from typing import List

game_folder = 'Pokemon Mystery Dungeon Explorers of Sky'
game_folder = 'Pokemon White 2'
overlay_file_path = os.path.join(NDS_TOOL_FOLDER, game_folder, 'y9.bin')
OVERLAY_LENGTH = 32

with open(overlay_file_path, 'rb') as overlay_file:
  overlay_data = overlay_file.read()

@dataclass
class Overlay:
  id: int
  address: int
  size: int

def read_long(start):
  data = overlay_data[start : start + 4]
  return struct.unpack_from('<l', data)[0]

overlays: List[Overlay] = []
for i in range(len(overlay_data) // OVERLAY_LENGTH):
  start = i * OVERLAY_LENGTH
  overlays.append(Overlay(read_long(start), read_long(start + 4), read_long(start + 8)))

for overlay in overlays:
  print(f'Overlay {overlay.id} ({hex(overlay.id)}), address {hex(overlay.address)}, size {overlay.size} ({hex(overlay.size)})')
