from music21 import *
import ashes
import sys

xmlName = sys.argv[1]

s = converter.parse(xmlName)
measureNumber = len(s.parts[0].getElementsByClass('Measure'))

for i in range(1, measureNumber+1):
	print(i)
	m = s.measure(i)
	ashesAnalysis = ashes.Ashes(m)
	if ashesAnalysis.isValidMeasure():
		step1 = ashesAnalysis.verticalMatch()
		step2 = ashesAnalysis.verticalMerge()
		step3 = ashesAnalysis.horizontalMerge()
		chordDict = ashesAnalysis.getChordinBeat()
		for part in m.parts[::-1]:
			for n in part.recurse().getElementsByClass('GeneralNote'):
				if (n.isNote or n.isChord) and n.beat in chordDict:
					n.addLyric(chordDict[n.beat].getPrintNotation() if chordDict[n.beat] else "N/A")
					del chordDict[n.beat]
s.show()