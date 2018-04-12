class ChordAnalyzingTool(object):

	def getChordNameList(self):
		return self._majorChordNameList + self._minorChordNameList

	def getTonicList(self):
		return self.majorTonicList + self._minorTonicList

	def getEnharmonicDictionary(self):
		return self._enharmonicDictionary

	def getReversedEnharmonicDictionary(self):
		return self._reversedEnharmonicDictionary

	def getIntervalDictionary(self):
		return self._intervalDictionary

	def getChordStructureDictionary(self):
		return self._chordStructureDictionary

	def getNoteOccurenceDictionary(self):
		return self._noteOccurenceDictionary

	def convertMatchTupleKeyToIndex(self, key=None):
		l = ['cname', 'chordType', 'inversion', 'roman', 'chordFunction', 'tonic', 'groupNo']
		if key in l:
			return l.index(key)
		else:
			return None

	# Result Structure
	# {tonic: ([totalmatch, ...], [exactmatch, ...], [possiblematch, ... )}
	#
	# totalmatch / exactmatch / possiblematch structure: tuple of (cname, chordType, inversion, roman, chordFunction, tonic, groupNo)

	def recognizeByAllTonic(self, interval):
		tonicList = self._majorTonicList + self._minorTonicList
		totalFlag = False
		result = {}
		for tonic in tonicList:
			tonicResult = self.__recognizeByTonic(tonic, interval.getChordRecognizerInputFormat())
			if tonicResult[2] == None:
				totalFlag = True
			result[tonic] = tonicResult
		if totalFlag:
			for x in result.keys():
				result[x] = (result[x][0], result[x][1], [])
		return result

	def __init__(self):		

		#storing common chord names
		self._majorChordNameList = [
			'I', 'I7', 
			'bII', 'II', 'II7', 
			'III', 'III7', 
			'IV', 'IV7', 
			'V', 'V7', 
			'bVI', 'gerVI', 'freVI', 'itaVI', 'VI', 'VI7', 
			'VII', 'VII7', 'dimVII7'
		]
		self._minorChordNameList = [
			'I', 'I+', 
			'bII', 'II', 'II7', 
			'III', 
			'IV', 'IV+', 
			'V', 'V+', 'V+7', 
			'VI', 'gerVI', 'freVI', 'itaVI', 
			'VII', 'dimVII', 'dimVII7'
		]

		
		#storing all possible tonics
		self._majorTonicList = ['C', 'G', 'D', 'A', 'E', 'B', 'Cb', 'F#', 'Gb', 'Db', 'C#', 'Ab', 'Eb', 'Bb', 'F']
		self._minorTonicList = ['Am', 'Em', 'Bm', 'F#m', 'C#m', 'G#m', 'Abm', 'D#m', 'Ebm', 'Bbm', 'A#m', 'Fm', 'Cm', 'Gm', 'Dm']

		
		#dictionary storing notes with same pitch
		self._enharmonicDictionary = {
			1: ['C', 'B#', 'Dbb'],
			2: ['C#', 'Db', 'B##'],
			3: ['D', 'Ebb', 'C##'],
			4: ['D#', 'Eb', 'Fbb'],
			5: ['E', 'Fb', 'D##'],
			6: ['F', 'E#', 'Gbb'],
			7: ['F#', 'Gb', 'E##'],
			8: ['G', 'Abb', 'F##'],
			9: ['G#', 'Ab', 'Ab'],
			10: ['A', 'Bbb', 'G##'],
			11: ['A#', 'Bb', 'Cbb'],
			12: ['B', 'Cb', 'A##'],
		}


		#reversed enharmonic dictionary for faster accessing by chord name
		d = {}
		for (key, cnameList) in self._enharmonicDictionary.items():
			for cname in cnameList:
				if cname not in d:
					d[cname] = key
		self._reversedEnharmonicDictionary = d


		# Roman dictionary, where key are the chord numbers, index of self._majorChordNameList / self._minorChordNameList
		self._majorRomanDictionary = {
			0: 'I', 1: 'I',
			2: 'bII', 3: 'II', 4: 'II',
			5: 'III', 6: 'III',
			7: 'IV', 8: 'IV',
			9: 'V', 10: 'V',
			11: 'bVI', 12: 'bVI', 13: 'bVI', 14: 'bVI', 15: 'VI', 16: 'VI',
			17: 'VII', 18: 'VII', 19: 'VII'
		}
		self._minorRomanDictionary = {
			0: 'I', 1: 'I',
			2: 'bII', 3: 'II', 4: 'II',
			5: 'bIII',
			6: 'IV', 7: 'IV',
			8: 'V', 9: 'V', 10: 'V',
			11: 'bVI', 12: 'bVI', 13: 'bVI', 14: 'bVI',
			15: 'bVII', 16: 'VII', 17: 'VII'
		}


		# chord type dictionary, where key are the chord numbers, index of self._majorChordNameList / self._minorChordNameList
		self._majorChordTypeDictionary = {
			0: 'Major', 1: 'Major 7th',
			2: 'Major', 3: 'Minor', 4: 'Minor 7th',
			5: 'Minor', 6: 'Minor 7th',
			7: 'Major', 8: 'Major 7th',
			9: 'Major', 10: 'Dominant 7th',
			11: 'Major', 12: 'German', 13: 'French', 14: 'Italian', 15: 'Minor', 16: 'Minor 7th',
			17: 'dim', 18: 'half-dim', 19: 'full-dim'
		}
		self._minorChordTypeDictionary = {
			0: 'Minor', 1: 'Major',
			2: 'Major', 3: 'dim', 4: 'half-dim',
			5: 'Major',
			6: 'Minor', 7: 'Major',
			8: 'Minor', 9: 'Major', 10: 'Dominant 7th',
			11: 'Major', 12: 'German', 13: 'French', 14: 'Italian',
			15: 'Major', 16: 'dim', 17: 'full-dim'
		}

		# chord function dictionary, where key are the chord numbers, index of self._majorChordNameList / self._minorChordNameList
		self._majorChordFunctionDictionary = {
			0: 'Tonic', 1: 'Tonic', 2: 'Undefined',
			3: 'Subdominant', 4: 'Subdominant', 
			5: 'Tonic', 6: 'Undefined', 7: 'Subdominant', 8: 'Undefined',
			9: 'Dominant', 10: 'Dominant',
			11: 'Subdominant', 12: 'Subdominant', 13: 'Subdominant', 14: 'Subdominant',
			15: 'Tonic', 16: 'Tonic',
			17: 'Dominant', 18: 'Dominant', 19: 'Dominant'
		}
		self._minorChordFunctionDictionary = {
			0: 'Tonic', 1: 'Tonic', 2: 'Undefined',
			3: 'Subdominant', 4: 'Subdominant', 5: 'Tonic',
			6: 'Subdominant', 7: 'Subdominant',
			8: 'Dominant', 9: 'Dominant', 10: 'Dominant',
			11: 'Subdominant', 12: 'Subdominant', 13: 'Subdominant', 14: 'Subdominant',
			15: 'Dominant', 16: 'Dominant', 17: 'Dominant'
		}

		
		#note interval dictionary
		d = {}
		for tonic in self._majorTonicList:
			e = self._reversedEnharmonicDictionary[tonic]
			d[tonic] = {}
			d[tonic]['P1'] = tonic
			d[tonic]['m2'] = self.__intervalCalculate(firstNote=tonic, targetNote=2, difference=(e + 1) % 12)
			d[tonic]['M2'] = self.__intervalCalculate(firstNote=tonic, targetNote=2, difference=(e + 2) % 12)
			d[tonic]['m3'] = self.__intervalCalculate(firstNote=tonic, targetNote=3, difference=(e + 3) % 12)
			d[tonic]['M3'] = self.__intervalCalculate(firstNote=tonic, targetNote=3, difference=(e + 4) % 12)
			d[tonic]['P4'] = self.__intervalCalculate(firstNote=tonic, targetNote=4, difference=(e + 5) % 12)
			d[tonic]['A4'] = self.__intervalCalculate(firstNote=tonic, targetNote=4, difference=(e + 6) % 12)
			d[tonic]['P5'] = self.__intervalCalculate(firstNote=tonic, targetNote=5, difference=(e + 7) % 12)
			d[tonic]['m6'] = self.__intervalCalculate(firstNote=tonic, targetNote=6, difference=(e + 8) % 12)
			d[tonic]['M6'] = self.__intervalCalculate(firstNote=tonic, targetNote=6, difference=(e + 9) % 12)
			d[tonic]['m7'] = self.__intervalCalculate(firstNote=tonic, targetNote=7, difference=(e + 10) % 12)
			d[tonic]['M7'] = self.__intervalCalculate(firstNote=tonic, targetNote=7, difference=(e + 11) % 12)
		for tonic in self._minorTonicList:
			tonicNote = tonic[:-1]
			e = self._reversedEnharmonicDictionary[tonicNote]
			d[tonic] = {}
			d[tonic]['P1'] = tonicNote
			d[tonic]['m2'] = self.__intervalCalculate(firstNote=tonicNote, targetNote=2, difference=(e + 1) % 12)
			d[tonic]['M2'] = self.__intervalCalculate(firstNote=tonicNote, targetNote=2, difference=(e + 2) % 12)
			d[tonic]['m3'] = self.__intervalCalculate(firstNote=tonicNote, targetNote=3, difference=(e + 3) % 12)
			d[tonic]['M3'] = self.__intervalCalculate(firstNote=tonicNote, targetNote=3, difference=(e + 4) % 12)
			d[tonic]['P4'] = self.__intervalCalculate(firstNote=tonicNote, targetNote=4, difference=(e + 5) % 12)
			d[tonic]['A4'] = self.__intervalCalculate(firstNote=tonicNote, targetNote=4, difference=(e + 6) % 12)
			d[tonic]['P5'] = self.__intervalCalculate(firstNote=tonicNote, targetNote=5, difference=(e + 7) % 12)
			d[tonic]['m6'] = self.__intervalCalculate(firstNote=tonicNote, targetNote=6, difference=(e + 8) % 12)
			d[tonic]['M6'] = self.__intervalCalculate(firstNote=tonicNote, targetNote=6, difference=(e + 9) % 12)
			d[tonic]['m7'] = self.__intervalCalculate(firstNote=tonicNote, targetNote=7, difference=(e + 10) % 12)
			d[tonic]['M7'] = self.__intervalCalculate(firstNote=tonicNote, targetNote=7, difference=(e + 11) % 12)
		self._intervalDictionary = d


		#chord structure dictionary
		d = {}
		for tonic in self._majorTonicList:
			i = self._intervalDictionary[tonic]
			c = self._majorChordNameList
			d[tonic] = {}
			d[tonic][c[0]] = (i['P1'], i['M3'], i['P5'])
			d[tonic][c[1]] = (i['P1'], i['M3'], i['P5'], i['M7'])
			d[tonic][c[2]] = (i['m2'], i['P4'], i['m6'])
			d[tonic][c[3]] = (i['M2'], i['P4'], i['M6'])
			d[tonic][c[4]] = (i['M2'], i['P4'], i['M6'], i['P1'])
			d[tonic][c[5]] = (i['M3'], i['P5'], i['M7'])
			d[tonic][c[6]] = (i['M3'], i['P5'], i['M7'], i['M2'])
			d[tonic][c[7]] = (i['P4'], i['M6'], i['P1'])
			d[tonic][c[8]] = (i['P4'], i['M6'], i['P1'], i['M3'])
			d[tonic][c[9]] = (i['P5'], i['M7'], i['M2'])
			d[tonic][c[10]] = (i['P5'], i['M7'], i['M2'], i['P4'])
			d[tonic][c[11]] = (i['m6'], i['P1'], i['m3'])
			d[tonic][c[12]] = (i['m6'], i['P1'], i['m3'], i['A4'])
			d[tonic][c[13]] = (i['m6'], i['P1'], i['M2'], i['A4'])
			d[tonic][c[14]] = (i['m6'], i['P1'], i['A4'])
			d[tonic][c[15]] = (i['M6'], i['P1'], i['M3'])
			d[tonic][c[16]] = (i['M6'], i['P1'], i['M3'], i['P5'])
			d[tonic][c[17]] = (i['M7'], i['M2'], i['P4'])
			d[tonic][c[18]] = (i['M7'], i['M2'], i['P4'], i['M6'])
			d[tonic][c[19]] = (i['M7'], i['M2'], i['P4'], i['m6'])
		for tonic in self._minorTonicList:
			tonicNote = tonic[:-1]
			i = self._intervalDictionary[tonic]
			c = self._minorChordNameList
			d[tonic] = {}
			d[tonic][c[0]] = (i['P1'], i['m3'], i['P5'])
			d[tonic][c[1]] = (i['P1'], i['M3'], i['P5'])
			d[tonic][c[2]] = (i['m2'], i['P4'], i['m6'])
			d[tonic][c[3]] = (i['M2'], i['P4'], i['m6'])
			d[tonic][c[4]] = (i['M2'], i['P4'], i['m6'], i['P1'])		
			d[tonic][c[5]] = (i['m3'], i['P5'], i['m7'])
			d[tonic][c[6]] = (i['P4'], i['m6'], i['P1'])	
			d[tonic][c[7]] = (i['P4'], i['M6'], i['P1'])
			d[tonic][c[8]] = (i['P5'], i['m7'], i['M2'])
			d[tonic][c[9]] = (i['P5'], i['M7'], i['M2'])
			d[tonic][c[10]] = (i['P5'], i['M7'], i['M2'], i['P4'])
			d[tonic][c[11]] = (i['m6'], i['P1'], i['m3'])
			d[tonic][c[12]] = (i['m6'], i['P1'], i['m3'], i['A4'])
			d[tonic][c[13]] = (i['m6'], i['P1'], i['M2'], i['A4'])
			d[tonic][c[14]] = (i['m6'], i['P1'], i['A4'])		
			d[tonic][c[15]] = (i['m7'], i['M2'], i['P4'])
			d[tonic][c[16]] = (i['M7'], i['M2'], i['P4'])
			d[tonic][c[17]] = (i['M7'], i['M2'], i['P4'], i['m6'])
		self._chordStructureDictionary = d


		#note occurence dictionary, for the occurence of specific notes in list of chords, indicate by chord number
		d = {}
		for tonic in self._majorTonicList:
			d[tonic] = {}
			i = self._intervalDictionary[tonic]
			d[tonic][i['P1']] = [0, 1, 4, 7, 8, 11, 12, 13, 14, 15, 16]
			d[tonic][i['m2']] = [2]
			d[tonic][i['M2']] = [3, 4, 6, 9, 10, 13, 17, 18, 19]
			d[tonic][i['m3']] = [11, 12]
			d[tonic][i['M3']] = [0, 1, 5, 6, 8, 15, 16]
			d[tonic][i['P4']] = [2, 3, 4, 7, 8, 10, 17, 18, 19]
			d[tonic][i['A4']] = [12, 13, 14]
			d[tonic][i['P5']] = [0, 1, 5, 6, 9, 10, 16]
			d[tonic][i['m6']] = [2, 11, 12, 13, 14, 19]
			d[tonic][i['M6']] = [3, 4, 7, 8, 15, 16, 18]
			d[tonic][i['M7']] = [1, 5, 6, 9, 10, 17, 18, 19]
		for tonic in self._minorTonicList:
			d[tonic] = {}
			i = self._intervalDictionary[tonic]
			d[tonic][i['P1']] = [0, 1, 4, 6, 7, 11, 12, 13, 14]
			d[tonic][i['m2']] = [2]
			d[tonic][i['M2']] = [3, 4, 8, 9, 10, 13, 15, 16, 17]
			d[tonic][i['m3']] = [0, 5, 11, 12]
			d[tonic][i['M3']] = [1]
			d[tonic][i['P4']] = [2, 3, 4, 6, 7, 10, 15, 16, 17]
			d[tonic][i['A4']] = [12, 13, 14]
			d[tonic][i['P5']] = [0, 1, 5, 8, 9, 10]
			d[tonic][i['m6']] = [2, 3, 4, 6, 11, 12, 13, 14, 17]
			d[tonic][i['M6']] = [7]
			d[tonic][i['m7']] = [5, 8, 15]
			d[tonic][i['M7']] = [9, 10, 16, 17]
		self._noteOccurenceDictionary = d


	# input structure
	# {note: frequency, note: frequency, ... }
	def __recognizeByTonic(self, tonic, inputDict):
		if tonic[-1] == 'm':
			minorMode = True
			tonicNote = tonic[:-1]
		else:
			minorMode = False
			tonicNote = tonic
		notemap = self._noteOccurenceDictionary[tonic]
		chord = self._chordStructureDictionary[tonic]
		notes = self._intervalDictionary[tonic]
		if minorMode:
			cname = self._minorChordNameList
			chordType = self._minorChordTypeDictionary
			roman = self._minorRomanDictionary
			cfunction = self._minorChordFunctionDictionary
			chordCount = [0] * 18
			occur = [0] * 18
			totalFound = [False] * 18
			chordgp = [0, 0, 1, 2, 2, 3, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 8, 8]
		else:
			cname = self._majorChordNameList
			chordType = self._majorChordTypeDictionary
			roman = self._majorRomanDictionary
			cfunction = self._majorChordFunctionDictionary
			chordCount = [0] * 20
			occur = [0] * 20
			totalFound = [False] * 20
			chordgp = [0, 0, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6, 6, 7, 7, 8, 8, 8]
		totalMatch = []
		exactMatch = []
		possibleMatch = []
		chordvalid = [0] * 9
		totalFlag = False
		cnote = inputDict.keys()
		if len(cnote) == 1:
			if tonicNote == cnote[0]:
				return ([], [], [(cname[0], chordType[0], 'Root', roman[0], cfunction[0], tonic, None)])
			else:
				return ([], [], [])

		for x in cnote:
			if x == notes['P1']:
				chordvalid[0] = 1
			elif x == notes['m2']:
				chordvalid[1] = 1
			elif x == notes['M2']:
				chordvalid[2] = 1
			elif x == notes['m3']:
				if minorMode:
					chordvalid[3] = 1
			elif x == notes['M3']:
				if not minorMode:
					chordvalid[3] = 1
			elif x == notes['P4']:
				chordvalid[4] = 1
			elif x == notes['P5']:
				chordvalid[5] = 1
			elif x == notes['m6']:
				chordvalid[6] = 1
			elif x == notes['M6']:
				if not minorMode:
					chordvalid[7] = 1
			elif x == notes['m7']:
				if minorMode:
					chordvalid[7] = 1
			elif x == notes['M7']:
				chordvalid[8] = 1
			try:
			 	for y in notemap[x]:
			 		chordCount[y] += 1
			except KeyError:
				pass
		#Exact match chords
		for x in range(len(cname)):
			if len(chord[cname[x]]) == 4 and chordCount[x] == 4:
				occur[x] = 1
				chordvalid[chordgp[x]] = 2
				if len(cnote) == 4:
					totalFound[x] = True
		for x in range(len(cname)):
			if len(chord[cname[x]]) == 3 and chordCount[x] == 3:
				occur[x] = 1
				chordvalid[chordgp[x]] = 2
				if (x == 4 or x == 14) and chordvalid[chordgp[x]] == 2:
					occur[x] = 0
				if len(cnote) == 3:
					totalFound[x] = True
		for x in range(len(cname)):
			if occur[x] == 1:
				inversion = self.__checkInversion(tonic=tonic, chordNo=x, inputs=inputDict)
				if totalFound[x]:
					totalMatch.append((inversion[0], chordType[x], inversion[1], roman[x], cfunction[x], tonic, None))
					totalFlag = True
				else:
					exactMatch.append((inversion[0], chordType[x], inversion[1], roman[x], cfunction[x], tonic, None))
				occur[x] = occur[x] + 1
		if totalFlag:
			return (totalMatch, exactMatch, None)
		#Possible match chords
		for x in range(len(cname)):
			if len(chord[cname[x]]) == 4 and chordCount[x] == 3 and occur[x] == 0 and chordvalid[chordgp[x]] == 1:
				occur[x] = 1
				chordvalid[chordgp[x]] = 2
		for x in range(len(cname)):
			if len(chord[cname[x]]) == 3 and chordCount[x] == 2 and occur[x] == 0 and chordvalid[chordgp[x]] == 1:
				occur[x] = 1
		for x in range(len(cname)):
			if occur[x] == 1:
				inversion = self.__checkInversion(tonic=tonic, chordNo=x, inputs=inputDict)
				possibleMatch.append((inversion[0], chordType[x], inversion[1], roman[x], cfunction[x], tonic, None))
		return (totalMatch, exactMatch, possibleMatch)


	def __checkInversion(self, tonic, chordNo, inputs):
		if tonic[-1] == 'm':
			cname = self._minorChordNameList
		else:
			cname = self._majorChordNameList
		chord = self._chordStructureDictionary[tonic]
		if chordNo in range(12, 15):
			return (cname[chordNo], 'Root')
		targetChord = chord[cname[chordNo]]
		is3 = len(targetChord) == 3
		inputSubset = {}
		for (key, value) in inputs.items():
			if key in targetChord:
				inputSubset[key] = value
		# for i in range(len(inputs.keys())):
		# 	if inputs.keys()[i] in targetChord:
		# 		inputSubset[inputs.keys()[i]] = inputs.values()[i]
		if len(inputSubset.keys()) < 2:
			return ('error', 'error')
		baseNote = inputSubset.keys()[inputSubset.values().index(min(inputSubset.values()))]
		if targetChord.index(baseNote) == 0:
			return (cname[chordNo], 'Root')
		elif targetChord.index(baseNote) == 1:
			if is3:
				return (cname[chordNo] + '6', '1st')
			else:
				return (cname[chordNo][:-1] + '65', '1st')
		elif targetChord.index(baseNote) == 2:
			if is3:
				return (cname[chordNo] + '64', '2nd')
			else:
				return (cname[chordNo][:-1] + '43', '2nd')
		elif targetChord.index(baseNote) == 3:
			#len(chord) must be four
			return (cname[chordNo][:-1] + '42', '3rd')


	def __intervalCalculate(self, firstNote, targetNote, difference):
		if(difference == 0):
			difference = 12
		choice = self._enharmonicDictionary[difference]
		for x in choice:
			diff = ord(x[0]) - ord(firstNote[0])
			if(diff < 0):
				diff += 7
			if (diff == targetNote - 1):
				return x
		return "Error"