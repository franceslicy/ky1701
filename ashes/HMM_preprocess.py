import ashes
from collections import Counter
from music21 import *

def toHMMvectors(m, mNumber, isTrain=False):
	a = ashes.Ashes(m)
	pitchCount = [Counter(sum([ashes.Ashes.getPitchesNorIndexOfNote(n) for n in a.grid[:,j]],[])) for j in range(a.grid.shape[1])]
	chordlabels = [next((n.lyrics[0].text for n in a.grid[:,j] if len(n.lyrics)==1 and n.lyrics[0].text), None) for j in range(a.grid.shape[1])]
	cutoffBeat = a.lowestMovementPart()[1]
	vectors = []
	accumulatePitch = Counter()
	currentChord = chordlabels[0]
	start_j = 0
	for j, beat in enumerate(a.beat):
		if not j==0 and beat in cutoffBeat:
			# add to vectors
			if isTrain:
				vectors.append(((mNumber, a.beat[start_j]),[(1 if accumulatePitch[i] else 0) for i in range(12)], currentChord))
			else:
				vectors.append(((mNumber, a.beat[start_j]),[(1 if accumulatePitch[i] else 0) for i in range(12)]))
			accumulatePitch = Counter()
			currentChord = chordlabels[j] or currentChord
			start_j = j
		accumulatePitch = accumulatePitch + pitchCount[j]
	return vectors

def preprocess(s, isTrain=False):
	measureNumber = len(s.parts[0].getElementsByClass('Measure'))
	normalized_data = []
	for mNumber in range(1,measureNumber+1):
		m = s.measure(mNumber)
		vector = toHMMvectors(m, mNumber, isTrain)
		normalized_data.append(vector)
	return normalized_data


# xmlName = sys.argv[1]
# isTrain = sys.argv[2] if len(sys.argv) == 3 else False
# s = converter.parse(xmlName)
# preprocess(s)