functions = [
  'ov29_02353530',
  'ov29_02353530',
  'ov29_02353530',
  'ov29_02353538',
  'ov29_0235171E',
  'ov29_0235177C',
  'ov29_02353538',
  'ov29_0235177C',
  'ov29_0235171E',
  'ov29_02353538',
  'ov10_022C4580',
  'ov10_022C4900',
  'ov29_02353538',
  'ov29_02353538',
  'ov29_02353538',
]

for function in sorted(set(functions)):
  print('.public ' + function)