major = [
	("I", {"Maj":"", "Maj7":"7"}),
	("II", {"min":"", "min7":"7", "-Maj":"b"}),
	("III", {"min":"", "min7":"7"}),
	("IV", {"Maj":"", "Maj7":"7"}),
	("V", {"Maj":"", "7":"7"}),
	("VI", {"-Maj":"b", "min":"", "min7":"7"}),
	("VII", {"dim":"", "dim7":"dim7", "It6":"Ita", "Ger6":"Ger", "Fr6":"Fre"}),
]
minor = [
	("I", {"Maj":"+", "min":""}),
	("II", {"-Maj":"b", "dim":"", "min7b5":"7"}),
	("III", {"Maj":""}),
	("IV", {"min":"", "Maj":"+"}),
	("V", {"min":"", "Maj":"+", "7":"+7"}),
	("VI", {"Maj":"b"}),
	("VII", {"-Maj":"", "dim":"dim", "dim7":"dim7", "It6":"Ita", "Ger6":"Ger", "Fr6":"Fre"}),
]
keys = {
	"CMajor": ["C","D","E","F","G","A","B"],
	"D-Major": ["D-","E-","F","G-","A-","B-","C"],
	"DMajor": ["D","E","F#","G","A","B","C#"],
	"E-Major": ["E-","F","G","A-","B-","C","D"],
	"EMajor": ["E","F#","G#","A","B","C#","D#"],
	"FMajor": ["F","G","A","B-","C","D","E"],
	"F#Major": ["F#","G#","A#","B","C#","D#","E#"],
	"G-Major": ["G-","A-","B-","C-","D-","E-","F"],
	"GMajor": ["G","A","B","C","D","E","F#"],
	"A-Major": ["A-","B-","C","D-","E-","F","G"],
	"AMajor": ["A","B","C#","D","E","F#","G#"],
	"B-Major": ["B-","C","D","E-","F","G","A"],
	"BMajor": ["B","C#","D#","E","F#","G#","A#"],
	"CMinor": ["C","D","E-","F","G","A-","B"],
	"D-Minor": ["D-","E-","F-","G-","A-","B--","C"],
	"DMinor": ["D","E","F","G","A","B-","C#"],
	"E-Minor": ["E-","F","G-","A-","B-","C-","D"],
	"EMinor": ["E","F#","G","A","B","C","D#"],
	"FMinor": ["F","G","A-","B-","C","D-","E"],
	"F#Minor": ["F#","G#","A","B","C#","D-","E#"],
	"G-Minor": ["G-","A-","B","C-","D-","E--","F"],
	"GMinor": ["G","A","B-","C","D","E-","F#"],
	"A-Minor": ["A-","B-","C-","D-","E-","F-","G"],
	"AMinor": ["A","B","C","D","E","F","G#"],
	"B-Minor": ["B-","C","D-","E-","F","G-","A"],
	"BMinor": ["B","C#","D","E","F#","G","A#"],
}

def changeChordLabel(s, keyDict):
	measureNumber = len(s.parts[0].getElementsByClass('Measure'))
	key = None
	for mNumber in range(1, measureNumber+1):
		m = s.measure(mNumber)
		labeledNotes = [n for p in m.parts for n in p.recurse().getElementsByClass("GeneralNote") if len(n.lyrics)==1 and n.lyrics[0].text]
		labeledNotes = sorted(labeledNotes, key=lambda x:x.beat)
		for i,n in enumerate(labeledNotes):
			chordName = n.lyrics[0].text
			# if mNumber in keyDict and i==0:
			# 	chordName += ":"+key
			if (mNumber,n.beat) in keyDict:
				key = keyDict[(mNumber,n.beat)]
			n.lyrics[0].text = toRomanNo(chordName, key, mNumber) + ","+key
	s.show()

# def changeChordLabel(s):
# 	measureNumber = len(s.parts[0].getElementsByClass('Measure'))
# 	key = None
# 	for mNumber in range(1, measureNumber+1):
# 		m = s.measure(mNumber)
# 		labeledNotes = [n for p in m.parts for n in p.recurse().getElementsByClass("GeneralNote") if len(n.lyrics)==1 and n.lyrics[0].text]
# 		labeledNotes = sorted(labeledNotes, key=lambda x:x.beat)
# 		for i,n in enumerate(labeledNotes):
# 			chordName = n.lyrics[0].text
# 			# if mNumber in keyDict and i==0:
# 			# 	chordName += ":"+key
# 			if "," in chordName:
# 				chord, key = chordName.split(',')
# 			else:
# 				chord = chordName
# 			if mNumber == 52: key = "B-Major"
# 			if mNumber == 58: key = "E-Major"
# 			if mNumber == 79: key = "A-Major"
# 			if mNumber == 94: key = "E-Major"
# 			if mNumber == 83: key = "B-Major"
# 			n.lyrics[0].text = chord + ","+key
# 	s.show()

def countToSharp(cnt):
	return ("#"*cnt if cnt > 0 else "-"*abs(cnt))

def sharpToCount(string):
	return string.count("#") - string.count("-")

def toRomanNo(chordName, key, mNumber):
	if chordName == "N/A":
		return "N/A"
	name = chordName[0] 
	cType = chordName[1:].replace('#','').replace('-','')
	romanIndex, root = next(((i,n) for i,n in enumerate(keys[key]) if n.startswith(name)),None)
	cType = countToSharp(sharpToCount(chordName[1:])-sharpToCount(root)) + cType

	roman, validList = (major if "Major" in key else minor)[romanIndex]
	if cType in validList:
		return roman+validList[cType]
	else:
		print(chordName,key,mNumber)
		return chordName


# xmlName = sys.argv[1]
# s = converter.parse(xmlName)
# keyDict = {}
# while True:
# 	raw_intput = input("measure number, key: ")
# 	if raw_intput:
# 		mNumber, key = raw_intput.split()
# 		keyDict[mNumber] = key
# 	else:
# 		break

# {(1,1):"GMinor",(23,1): "DMajor",(29,1): "B-Major",(53,1): "FMinor",(59,1): "B-Major",(70,4): "FMajor",(71,2):"B-Major",(83,1):"GMinor",(93,1): "DMinor",(96,1): "AMinor", (103,1): "DMinor", (107,1): "DMajor", (109,1): "GMinor", (139,1): "DMajor", (145,1): "GMinor", (169,1): "CMinor", (174,1): "DMajor", (177,1): "GMinor",(188,4):"DMajor",(189,2):"GMinor",(204,1):"CMinor",(207,3):"GMinor"}

# {(1,1):"FMajor",(2,1):"CMajor",(3,1):"GMajor",(5,1):"CMajor",(18,1):"DMinor",(24,1):"CMajor",(53,1):"GMajor",(64,1):"CMajor",(68,1):"GMajor",(74,1):"CMajor",(74,2.5):"DMajor",(75,1):"GMajor",(77,1):"GMinor",(86,1):"GMajor",(93,1):"EMajor",(95,1):"AMinor",(97,1):"DMajor",(100,1):"GMajor",(107,1):"CMajor",}
