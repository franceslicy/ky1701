import sys
from music21 import *
import chordIdentification

def preProcess(s):
	ns = s.voicesToParts().sliceByBeat()
	ns.parts[-3].transpose(interval.Interval('-M6'), inPlace=True)
	return ns

xmlName = sys.argv[1]

s = converter.parse(xmlName)
key = s.analyze('key')
measureNumber = len(s.parts[0].getElementsByClass('Measure'))
measureNumber = 64
ns = preProcess(s)

for a in range(1,measureNumber+1):
	m = ns.measure(a)
	print('measureNumber:'+str(a))
	measureChord = chordIdentification.getChordInTime(key,m)
	# print('\n')

	# measure cut
	strongBeats = [n.beat for n in m.parts[0].recurse().notesAndRests if n.beatStrength>=0.5]
	subSegmentChords = []
	if len(strongBeats) > 1:
		for i,b in enumerate(strongBeats):
			if i == len(strongBeats) - 1:
				subSegmentChords.append(chordIdentification.getChordInTime(key,m,b))
			else:
				subSegmentChords.append(chordIdentification.getChordInTime(key,m,b,strongBeats[i+1]))

	# print('result:')
	# print(measureChord,subSegmentChords)
	if sum(a[1] < measureChord[1] for a in subSegmentChords) > 0:
		print(measureChord)
	else:
		print(subSegmentChords)
	print('\n')