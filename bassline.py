import sys
from music21 import *

# get lowest voice
# if no notes, search lowest in measure

def highlightArrayNotes(notes):
	for note in notes:
		if hasattr(note, 'style') and hasattr(note.style, 'color'):
			note.style.color = 'red'

def getAvgPitchOfPart(part):
	totalNotes = 0
	totalHeight = 0
	for note in part.recurse().getElementsByClass('Note'):
		totalNotes += 1
		totalHeight += note.pitch.ps
	return totalHeight/totalNotes

def getPartListLowest(score):
	parts = score.parts
	pitchOfParts = {}
	if len(parts) == 1: return [0]
	for i in range(0, len(parts)):
		pitchOfParts[i] = getAvgPitchOfPart(parts[i])
	pitchOfParts = sorted(pitchOfParts, key=pitchOfParts.get)
	return pitchOfParts

def showBaseline(score):
	partIndicesOrdered = getPartListLowest(score)
	print (partIndicesOrdered)
	lowestPart = score.parts[partIndicesOrdered[0]]
	measureCount = len(lowestPart.getElementsByClass('Measure'))
	for i in range(0, measureCount):
		baseMeasure = stream.Measure()
		for index in partIndicesOrdered:
			baseMeasure = score.parts[index].measure(i+1)
			if len(baseMeasure.recurse().notes) > 0: break
		highlightArrayNotes(baseMeasure.recurse().notesAndRests)


s = converter.parse(sys.argv[1])
# s = corpus.parse('bach/bwv66.6')
showBaseline(s)
s.show()