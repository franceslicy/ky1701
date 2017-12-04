from music21 import *
import chordMatch

def getIntervalGroupOfNotes(n1, n2):
	if n1.isRest or n2.isRest: return None
	if not n1.isChord: n1 = [n1]
	if not n2.isChord: n2 = [n2]
	# rearrange
	if len(n2) > len(n1):
		temp = n1
		n1 = n2
		n2 = temp

	n2Length = len(n2)

	intervalList = []
	for index, n in enumerate(n1):
		if n2Length>index:
			intervalList.append(interval.Interval(n, n2[index]))
		else:
			intervalList.append(interval.Interval(n, n2[-1]))
	return intervalList

def getIntervalList(noteList):
	listLength = len(noteList)
	intervalList = []
	for index, n1 in enumerate(noteList):
		if index == listLength - 1: break
		n2 = noteList[index+1]
		# rule: if n1 is None, get previous one.
		while n1.isRest and index > 0: 
			index -= 1
			n1 = noteList[index]
		if n1.isRest or n2.isRest:
			intervalList.append(None)
		else:
			intervalList.append(getIntervalGroupOfNotes(n1, n2))
	return intervalList

def previousNote(n):
	preN = n
	for a in range(5):
		if preN is None:
			break
		preN = preN.previous()
		if isinstance(preN, note.GeneralNote) and preN.id != n.id:
			return preN
			break
	return None
	# pn = n.previous('Note');
	# if pn is None and n.derivation.origin is not None:
	# 	origin = n.derivation.origin
	# 	return origin.previous('Note')
	# else:
	# 	return pn

def nextNote(n):
	nextN = n
	for a in range(5):
		if nextN is None:
			break
		nextN = nextN.next()
		if isinstance(nextN, note.GeneralNote) and nextN.id != n.id:
			return nextN
			break
	return None
	# pn = n.next('Note');
	# if pn is None and n.derivation.origin is not None:
	# 	origin = n.derivation.origin
	# 	return origin.next('Note')
	# else:
	# 	return pn

def getNoteInChord(c, index=None):
	if index is not None and len(c) > index:
		return c[index]
	return None

# def noteIsInStep(n, index=None):
# 	preN = previousNote(n)
# 	if preN is not None and interval.Interval(n, preN).isStep:
# 		return True
# 	nextN = nextNote(n)
# 	if nextN is not None and interval.Interval(n, nextN).isStep:
# 		return True
# 	return False

# def noteIsInSame(n, index=None):
# 	if n.isChord:
# 		n = getNoteInChord(n, index)
# 		if n is None: return False
# 	preN = previousNote(n)
# 	if preN is not None:
# 		if preN.isChord:
# 			# if has index getNoteInChord else 
# 			if index
# 		elif n.pitch == preN.pitch:
# 			return True
# 	nextN = nextNote(n)
# 	if nextN is not None and n.pitch == nextN.pitch:
# 		return True
# 	return False

def getIntervalsOfSize(inIntervalList, size):
	if inIntervalList is None: return None
	inIntervalLength = len(inIntervalList)
	if size == inIntervalLength:
		return inIntervalList
	outIntervalList = []
	for index in range(size):
		if not index == size-1:
			outIntervalList.append(inIntervalList[index])
		else:
			outIntervalList.append(min(inIntervalList[index:], key=lambda a: a.semitones))
	return outIntervalList

def getStepWeight(intervalList, noteList):
	# todo: prevent error (len(intervalList) vs len(noteList))
	listLength = len(intervalList)
	weightList = [[0]] * (listLength-1)
	for index, n in enumerate(noteList):
		if n.isRest:
			continue 
		if not n.isChord: n = [n]
		# intervals with previous note / chord
		l1 = intervalList[index]
		if index==0: l1 = None 		# not consider step with previous segment
		intervalList1 = getIntervalsOfSize(l1, len(n))


		# intervals with next note / chord
		index2 = index+1
		l2 = intervalList[index2]
		while l2 is None and index2 < listLength-1:
			index2 += 1
			l2 = intervalList[index2]
		if index2==listLength-1: l2 = None 		# not consider step with previous segment
		intervalList2 = getIntervalsOfSize(l2, len(n))

		weightList_note = [1] * len(n)
		if intervalList1 is not None:
			for index_note, interval1 in enumerate(intervalList1):
				if isinstance(interval1, interval.Interval) and interval1.isStep:
					weightList_note[index_note] = 0
		if intervalList2 is not None:
			for index_note, interval2 in enumerate(intervalList2):
				if isinstance(interval2, interval.Interval) and interval2.isStep:
					weightList_note[index_note] = 0
		
		weightList[index] = weightList_note
	return weightList

		
	# for index, interval1 in enumerate(intervalList):
	# 	if isinstance(interval1, interval.Interval) and interval1.isStep:
	# 		if index > 0:
	# 			weightList[index-1] += 1
	# 		if index < listLength-1:
	# 			weightList[index] += 1
	# return weightList

def getRepeatWeight(noteList, preN, nextN):
	listLength = len(noteList)
	weightList = [[0]] * listLength

	# from front to end
	if preN.isRest: preN = []
	elif not preN.isChord: preN = [preN]
	holding_pitchSet = set([a.pitch for a in preN])
	for index, n in enumerate(noteList):
		if n.isRest:
			continue
		if not n.isChord: n = [n]
		if holding_pitchSet:
			holding_pitchSet = holding_pitchSet & set([a.pitch for a in n])
			weightList_note = [1 if a.pitch in holding_pitchSet else 100 for a in n]
		else:
			weightList_note = [100 for a in n]
		weightList[index] = weightList_note
	
	# from end to front
	if nextN.isRest: nextN = []
	elif not nextN.isChord: nextN = [nextN]
	holding_pitchSet = set([a.pitch for a in nextN])
	for index, n in enumerate(noteList[::-1]):
		if n.isRest:
			continue
		if not n.isChord: n = [n]
		if holding_pitchSet:
			holding_pitchSet = holding_pitchSet & set([a.pitch for a in n])
			weightList_note = [1 if a.pitch in holding_pitchSet else 100 for a in n]
			weightList_note = [min(a,b) for a,b in zip(weightList_note, weightList[-(index+1)])]
		else:
			break
		weightList[-(index+1)] = weightList_note
	return weightList


# def getRepeatWeight(intervalList, noteList):
# 	listLength = len(intervalList)
# 	weightList = [[0]] * (listLength-1)
# 	for index, n in enumerate(noteList):
# 		if n.isRest:
# 			continue
# 		l1 = intervalList[index]
# 		intervalList1 = getIntervalsOfSize(l1, len(n))

# 		weightList_note = [0] * len(n)
# 		if intervalList1 is not None:
# 			for index_note, interval1 in enumerate(intervalList1):
# 				if isinstance(interval1, interval.Interval) and interval1.semitones == 0:
# 					weightList_note[index_note] += 1
# 					holding_note = interval1.noteStart
# 		weightList[index] = weightList_note

# 	for index, n in enumerate(noteList[::-1]):
# 		if n.isRest:
# 			continue
# 		index2 = -(index+1)
# 		l2 = intervalList[index2]
# 		while l2 is None and ++index2 < 0:
# 			l2 = intervalList[index2]
# 		intervalList2 = getIntervalsOfSize(l2, len(n))

# 		weightList_note = weightList[-(index+1)]
# 		if intervalList2 is not None:
# 			for index_note, interval2 in enumerate(intervalList2):
# 				if isinstance(interval2, interval.Interval) and interval2.semitones == 0:
# 					weightList_note[index_note] += 1
# 		weightList[-(index+1)] = weightList_note
# 	return weightList

# 	for index, interval1 in enumerate(intervalList):
# 		if index == listLength-1:
# 			break
# 		if interval1.semitones == 0:
# 			weightList[index] = 1
# 		else:
# 			break
# 	for index, interval1 in enumerate(intervalList[::-1]):
# 		if index == listLength-1:
# 			break
# 		if interval1.semitones == 0:
# 			weightList[-(index+1)] = 1
# 		else:
# 			break
# 	return weightList

def getDurationWeight(noteList):
	weightList = [[0]] * len(noteList)
	for index, n in enumerate(noteList):
		if n.isRest:
			continue
		if n.isChord:
			weightList[index] = [n.duration.quarterLength] * len(n)
		else:
			weightList[index] = [n.duration.quarterLength]
	return weightList

def getPitchList(noteList):
	pitchList = []
	for n in noteList:
		if n.isRest:
			pitchList.append([None])
		elif n.isChord:
			pitchList.append([a.name for a in n])
		else:
			pitchList.append([n.name])
	return pitchList

def getWeightOfNotes(notesDict, groupedScore):
	for t in groupedScore:
		if t[0] == None or t[1] == 0:
			continue
		if t[0] in notesDict:
			notesDict[t[0]] += t[1]
		else:
			notesDict[t[0]] = t[1]
	return notesDict

def getPossibleChords(pitchWeight, tonicNote, scale):
	pitchList = sorted(pitchWeight, key=pitchWeight.get, reverse=True)
	sub_dict = chordMatch.major_chord_tree if scale=="major" else chordMatch.minor_chord_tree
	best_index = -1

	for index,p in enumerate(pitchList):
		n = note.Note(p)
		n.octave = None
		i = interval.Interval(tonicNote, n)
		if tonicNote != n and interval.getWrittenLowerNote(tonicNote, n) == n:
			i = i.complement
		if i.name not in sub_dict:
			break
		best_index = index
		sub_dict = sub_dict[i.name]

	result = sub_dict['result']
	exclude = pitchList[best_index+1:]

	return result

def normalizePitchDict(pitchDict, tonicNote):
	nPitchDict = {}
	for index, value in pitchDict.items():
		n = note.Note(index)
		i = interval.Interval(tonicNote,n)
		if tonicNote != n and interval.getWrittenLowerNote(tonicNote, n) == n:
			i = i.complement
		nPitchDict[i.name] = value
	return nPitchDict

def getScoreOfChord(chordName, nPitchDuration, scale):
	totalScore = 0;
	inChordScore = 0;
	chordnPitch = (chordMatch.major_chord if scale=="major" else chordMatch.minor_chord)[chordName]
	for nPitch, value in nPitchDuration.items():
		if nPitch in chordnPitch:
			inChordScore += value
		totalScore += value
	inclusionScore = sum(a in nPitchDuration for a in chordnPitch)
	return (((inChordScore/totalScore) if totalScore>0 else 0), inclusionScore/len(chordnPitch))




def getChordInTime(key, measure, startBeat=1, endBeat=None):	 # score should be voicesToParts & sliceByBeat
	pitchWeight = {}
	pitchDuration = {}
	for p in measure.recurse().getElementsByClass('Part'):
		if endBeat is None:
			notesInBeat = [n for n in p.recurse().notesAndRests if n.beat >= startBeat]
		else:
			notesInBeat = [n for n in p.recurse().notesAndRests if n.beat >= startBeat and n.beat < endBeat]
		if len([n for n in notesInBeat if not n.isRest]) > 0:
			# find previous & next
			preN = previousNote(notesInBeat[0]) or note.Rest()
			nextN = nextNote(notesInBeat[-1]) or note.Rest()
			intervalList = getIntervalList([preN] + notesInBeat + [nextN])
			stepWeight = getStepWeight(intervalList, notesInBeat)
			repeatWeight = getRepeatWeight(notesInBeat, preN, nextN)
			durationWeight = getDurationWeight(notesInBeat)
			pitchList = getPitchList(notesInBeat)
			# print(intervalList, pitchList, stepWeight, repeatWeight, durationWeight)
			# pitchScoreTuple = [(a,b*c*d) for w,x,y,z in zip(pitchList, stepWeight, repeatWeight, durationWeight) for a,b,c,d in zip(w,x,y,z)]
			pitchScoreTuple = [(a,b*c) for w,x,y in zip(pitchList, stepWeight, durationWeight) for a,b,c in zip(w,x,y)]
			noteDurationTuple = [(a,b) for x,y in zip(pitchList, durationWeight) for a,b in zip(x,y)]
			pitchWeight = getWeightOfNotes(pitchWeight, pitchScoreTuple)
			print(pitchScoreTuple)
			pitchDuration = getWeightOfNotes(pitchDuration, noteDurationTuple)
			# print('\n')
	# print(pitchWeight)
	# chord matching
	tonicNote = note.Note(key.getTonic())
	tonicNote.octave = None
	scale = key.mode
	possibleChords = getPossibleChords(pitchWeight, tonicNote, scale)
	# score calculation
	if possibleChords:
		nPitchDuration = normalizePitchDict(pitchDuration, tonicNote)
		chordScores = {a: getScoreOfChord(a,nPitchDuration, scale) for a in possibleChords}
		# print(nPitchDuration)
		# print(chordScores)
		bestChord = max(chordScores, key=chordScores.get)
		return (bestChord,chordScores[bestChord])
	else:
		return (None,(0,0))

		# if len(notesInBeat) > 1:
		# 	# find if step
		# 	# remove running notes

		# elif len(notesInBeat) == 1:
		# 	# is a step or not
		# 	# add to weightedList
		# 	n = notesInBeat[0]
		# 	pitch = n.pitch
		# 	duration = endBeat - n.beat
		# 	weightedList[pitch.name] = 