from pprint import *
major_chord = {
  'I': [
    ['C', 'E', 'G'],
    ['C', 'E'],
    ['C', 'G'],
    ['E', 'G']
  ],
  'I 7': [
    ['C', 'E', 'G', 'B'],
    ['C', 'E', 'B'],
    ['C', 'G', 'B'],
    ['E', 'G', 'B'],
    ['C', 'B'],
    ['E', 'B'],
    ['G', 'B']
  ],
  'II': [
    ['D', 'F', 'A'],
    ['D', 'F'],
    ['D', 'A'],
    ['F', 'A']
  ],
  'II 7': [
    ['D', 'F', 'A', 'C'],
    ['D', 'F', 'C'],
    ['D', 'A', 'C'],
    ['F', 'A', 'C'],
    ['D', 'C'],
    ['F', 'C'],
    ['A', 'C']
  ],
  'II b': [
    ['Db', 'F', 'Ab'],
    ['Db', 'F'],
    ['Db', 'Ab'],
    ['F', 'Ab']
  ],
  'III': [
    ['E', 'G', 'B'],
    ['E', 'G'],
    ['E', 'B'],
    ['G', 'B']
  ],
  'III 7': [
    ['E', 'G', 'B', 'D'],
    ['E', 'G', 'D'],
    ['E', 'B', 'D'],
    ['G', 'B', 'D'],
    ['E', 'D'],
    ['G', 'D'],
    ['B', 'D']
  ],
  'IV': [
    ['F', 'A', 'C'],
    ['F', 'A'],
    ['F', 'C'],
    ['A', 'C']
  ],
  'IV 7': [
    ['F', 'A', 'C', 'E'],
    ['F', 'A', 'E'],
    ['F', 'C', 'E'],
    ['A', 'C', 'E'],    # VII
    ['F', 'E'],
    ['A', 'E'],
    ['C', 'E']
  ],
  'V': [
    ['G', 'B', 'D'],
    ['G', 'B'],
    ['G', 'D'],
    ['B', 'D']
  ],
  'V 7': [
    ['G', 'B', 'D', 'F'],
    ['G', 'B', 'F'],
    ['G', 'D', 'F'],
    ['B', 'D', 'F'],
    ['G', 'F'],
    ['B', 'F'],
    ['D', 'F']
  ],
  'VI': [
    ['A', 'C', 'E'],
    ['A', 'C'],
    ['A', 'E'],
    ['C', 'E']
  ],
  'VI 7': [
    ['A', 'C', 'E', 'G'],
    ['A', 'C', 'G'],
    ['A', 'E', 'G'],
    ['C', 'E', 'G'],
    ['A', 'G'],
    ['C', 'G'],
    ['E', 'G']
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
    ['B', 'D', 'F'],
    ['B', 'D'],
    ['B', 'F'],
    ['D', 'F']
  ],
  'VII 7': [
    ['B', 'D', 'F', 'A'],
    ['B', 'D', 'A'],
    ['B', 'F', 'A'],
    ['D', 'F', 'A'],
    ['B', 'A'],
    ['D', 'A'],
    ['F', 'A']
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
notes = ['C','Db','D','Eb','E','F','F#','G','Ab','A','B']

# for note in notes:
#   sub_dict = {}
#   for notat, chords in major_chord.items():
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
      if 1:
        main_dict[note] = iterate(exclude_notes+[note], note_dict)
  # check for exact result
  for notat, chords in chord_dict.items():
    chords_exact = [x for x in chords if sorted(exclude_notes) == sorted(x)]
    if len(chords_exact) > 0:
      main_dict['result'].append(notat)
  return main_dict

new_dict = iterate([], major_chord)
# def pretty(d, indent=0):
#    for key, value in d.items():
#       print(' ' * indent + str(key))
#       if isinstance(value, dict):
#          pretty(value, indent+1)
#       else:
#          print(' ' * (indent+1) + str(value))
# pretty(new_dict, 2)
pprint(new_dict)