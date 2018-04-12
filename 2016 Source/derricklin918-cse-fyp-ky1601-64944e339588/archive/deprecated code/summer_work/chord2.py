from music21 import *
import numpy as np
    
c = converter.parse('/Users/derricklin/Development/piano-reduction/chord-identification/chord-2.xml')
p = c.parts
for part in p:
    part.show('text')
    print (part.id);


# m1 = p[0].getElementsByClass('Measure')
# b1 = m1[0].getElementsByClass(note.Note)
# b1.show('text')
