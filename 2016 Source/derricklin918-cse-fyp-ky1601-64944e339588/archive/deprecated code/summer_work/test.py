from music21 import *

p1 = stream.Part()
k1 = key.KeySignature(1)
n1 = note.Note('B')
r1 = note.Rest()
c1 = chord.Chord(['A', 'B-'])
p1.append([n1, k1, c1, r1])
p1.show('musicxml')
