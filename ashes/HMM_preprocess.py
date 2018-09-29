import ashes
import sys
from collections import Counter
from music21 import *

major_list = ["CMajor","D-Major","DMajor","E-Major","EMajor","FMajor","G-Major","GMajor","A-Major","AMajor","B-Major","BMajor"]
minor_list = ["CMinor","D-Minor","DMinor","E-Minor","EMinor","FMinor","G-Minor","GMinor","A-Minor","AMinor","B-Minor","BMinor"]

def toHMMvectors(m, mNumber, isTrain=False):
	a = ashes.Ashes(m)
	if not a.isValidMeasure():
		return None
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
	if isTrain:
		vectors.append(((mNumber, a.beat[start_j]),[(1 if accumulatePitch[i] else 0) for i in range(12)], currentChord))
	else:
		vectors.append(((mNumber, a.beat[start_j]),[(1 if accumulatePitch[i] else 0) for i in range(12)]))
	
	return vectors

def normalizeByKey(vector_list):
	currentKey = None
	accumulateVector = []
	accumulateVector_samekey = []
	for index,pitches,label in vector_list:
		if label is None:
			key = currentKey 
		else:
			key = label.split(",")[1]
		shift_index = major_list.index(key) if key in major_list else minor_list.index(key)
		normalizePitches = pitches[shift_index:] + pitches[:shift_index]
		if currentKey == key or not accumulateVector_samekey:
			accumulateVector_samekey.append((index,normalizePitches,label))
		else:
			accumulateVector.append(accumulateVector_samekey)
			accumulateVector_samekey = [(index,normalizePitches,label)]
		currentKey = key
	accumulateVector.append(accumulateVector_samekey)
	return accumulateVector


def preprocess(s, isTrain=True):
	measureNumber = len(s.parts[0].getElementsByClass('Measure'))
	normalized_data = []
	for mNumber in range(1,measureNumber+1):
		m = s.measure(mNumber)
		vector = toHMMvectors(m, mNumber, isTrain)
		if vector:
			normalized_data.extend(vector)
	if isTrain:
		normalized_data = normalizeByKey(normalized_data)
	return normalized_data

if __name__ == '__main__':
    xmlName = sys.argv[1]
    isTrain = True if len(sys.argv) == 3 and sys.argv[2] in ['1', 'True', 'true'] else False
    s = converter.parse(xmlName)
    pre = preprocess(s, isTrain)
    print(len(pre))
    f = open(xmlName[:-4]+".txt", "w")
    if isTrain == True:
        for vec in pre:
            for i in vec:
                if len(i) == 3:
                    f.write(str(i[0]) + " | " + str(i[1]) + " | " + str(i[2]) + "\n")
    else:
        for vec in pre:
             f.write(str(vec[0]) + " | " + str(vec[1]) + "\n")
    f.close()