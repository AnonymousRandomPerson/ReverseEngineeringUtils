functions = [
  'sub_0207CD44',
  'sub_02079DE0',
  'sub_02079DE0',
  'ov00_022D4B88',
  'ov00_022D4B88',
  'Strcpy',
  'ov00_022CEF10',
  'ov00_022CF8F8',
  'Strcpy',
  'ov02_0233C114',
]

for function in set(functions):
  print('.public ' + function)