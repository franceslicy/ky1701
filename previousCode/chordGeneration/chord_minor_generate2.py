from pprint import *
minor_chord = {
  'I': [
    ['C', 'Eb', 'G'], 
    ['C', 'Eb'], 
    ['C', 'G'], 
    ['Eb', 'G']
  ],
  'I +': [
    ['C', 'E', 'G'], 
    ['C', 'E'], 
    ['C', 'G'], 
    ['E', 'G']
  ],
  'II': [
    ['D', 'F', 'Ab'], 
    ['D', 'F'], 
    ['D', 'Ab'], 
    ['F', 'Ab']
  ],
  'II 7': [
    ['D', 'F', 'Ab', 'C'],
    ['D', 'F', 'C'],
    ['D', 'Ab', 'C'],
    ['F', 'Ab', 'C'],
    ['D', 'C'],
    ['F', 'C'],
    ['Ab', 'C']
  ],
  'II b': [
    ['Db', 'F', 'Ab'], 
    ['Db', 'F'], 
    ['Db', 'Ab'], 
    ['F', 'Ab']
  ],
  'III': [
    ['Eb', 'G', 'Bb'], 
    ['Eb', 'G'], 
    ['Eb', 'Bb'], 
    ['G', 'Bb']
  ],
  'IV': [
    ['F', 'Ab', 'C'], 
    ['F', 'Ab'], 
    ['F', 'C'], 
    ['Ab', 'C']
  ],
  'IV +': [
    ['F', 'A', 'C'], 
    ['F', 'A'], 
    ['F', 'C'], 
    ['A', 'C']
  ],
  'V': [
    ['G', 'Bb', 'D'], 
    ['G', 'Bb'], 
    ['G', 'D'], 
    ['Bb', 'D']
  ],
  'V +': [
    ['G', 'B', 'D'], 
    ['G', 'B'], 
    ['G', 'D'], 
    ['B', 'D']
  ],
  'V +7': [
    ['G', 'B', 'D', 'F'],
    ['G', 'B', 'F'],
    ['G', 'D', 'F'],
    ['B', 'D', 'F'],
    ['G', 'F'],
    ['B', 'F'],
    ['D', 'F']
  ],
  'VI Fre': [
    ['Ab', 'C', 'D', 'F#'],
    ['Ab', 'C', 'D'],
    ['Ab', 'D', 'F#'],
    ['C', 'D', 'F#'],
    ['Ab', 'D'],
    ['C', 'D'],
    ['D', 'F#']
  ],
  'VI Ger': [
    ['Ab', 'C', 'Eb', 'F#'],
    ['Ab', 'Eb', 'F#'],
    ['C', 'Eb', 'F#'],
    ['Eb', 'F#']
  ],
  'VI Ita': [
    ['Ab', 'C', 'F#'], 
    ['Ab', 'F#'], 
    ['C', 'F#']
  ],
  'VI b': [
    ['Ab', 'C', 'Eb'], 
    ['Ab', 'C'], 
    ['Ab', 'Eb'], 
    ['C', 'Eb']
  ],
  'VII': [
    ['Bb', 'D', 'F'], 
    ['Bb', 'D'], 
    ['Bb', 'F'], 
    ['D', 'F']
  ],
  'VII dim': [
    ['B', 'D', 'F'], 
    ['B', 'D'], 
    ['B', 'F'], 
    ['D', 'F']
  ],
  'VII dim7': [
    ['B', 'D', 'F', 'Ab'],
    ['B', 'D', 'Ab'],
    ['B', 'F', 'Ab'],
    ['D', 'F', 'Ab'],
    ['B', 'Ab'],
    ['D', 'Ab'],
    ['F', 'Ab']
  ]
}

new_dict = {}
notes = ['C','Db','D','Eb','E','F','F#','G','Ab','A','Bb','B']

# for note in notes:
#   sub_dict = {}
#   for notat, chords in minor_chord.items():
#     chords_have_note = list(filter(lambda x: note in x, chords))
#     if len(chords_have_note) > 0:
#       sub_dict[notat] = chords_have_note
#   new_dict[note] = sub_dict
# pprint(new_dict)

def iterate(exclude_notes, chord_dict):
  included_notes = [x for x in notes if x not in exclude_notes]
  main_dict = {}
  main_dict['result'] = []
  # if only one entry in chord_dict
  # if len(chord_dict) == 1:
  #   notat = list(chord_dict.keys())[0]
  #   chords = chord_dict[notat]
  #   main_dict['result'].append(notat)
  #   return main_dict
  # map to sub note tree
  for note in included_notes:
    note_dict = {}
    for notat, chords in chord_dict.items():
      chords_have_note = [x for x in chords if note in x]
      if len(chords_have_note) > 0:
        note_dict[notat] = chords_have_note
    if len(note_dict) > 0:
        main_dict[note] = iterate(exclude_notes+[note], note_dict)
  # check for exact result
  for notat, chords in chord_dict.items():
    chords_exact = [x for x in chords if sorted(exclude_notes) == sorted(x)]
    if len(chords_exact) > 0:
      main_dict['result'].append(notat)
  return main_dict

new_dict = iterate([], minor_chord)
# def pretty(d, indent=0):
#    for key, value in d.items():
#       print(' ' * indent + str(key))
#       if isinstance(value, dict):
#          pretty(value, indent+1)
#       else:
#          print(' ' * (indent+1) + str(value))
# pretty(new_dict, 2)
pprint(new_dict)