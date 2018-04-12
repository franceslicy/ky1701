from music21 import *

c = converter.parse('/Users/derricklin/Development/piano-reduction/chord-identification/chord-1.xml')
# get the first note
p = c.getElementsByClass(stream.Part)[0].getElementsByClass(stream.Measure)[0].getElementsByClass(note.Note)[0]
print(p)
print(p.pitch.ps)
