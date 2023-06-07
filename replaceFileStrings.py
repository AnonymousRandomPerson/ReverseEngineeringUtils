import os

with open(os.path.join('pointer', 'raw.txt'), 'r') as raw_file:
  raw_text = raw_file.read()

raw_text = raw_text.replace('.byte 0x70, 0x6b, 0x73, 0x64, 0x69, 0x72, 0x30, 0x00,', '.string "pksdir0\\0"\n.byte')
raw_text = raw_text.replace('.byte 0x53, 0x49, 0x52, 0x4f,', '.string "SIRO"\n.byte')
raw_text = raw_text.replace(', 0x53, 0x49, 0x52, 0x4f,', '\n.string "SIRO"\n.byte')
raw_text = raw_text.replace(', 0x53, 0x49, 0x52, 0x4f', '\n.string "SIRO"')
raw_text = raw_text.replace('.byte 0x41, 0x54, 0x34, 0x50, 0x58,', '.string "AT4PX"\n.byte')

with open(os.path.join('pointer', 'transformed.txt'), 'w') as transformed_file:
  transformed_file.write(raw_text)