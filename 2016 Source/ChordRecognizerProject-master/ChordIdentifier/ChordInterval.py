import re

class ChordInterval(object):

	# ChordInterval Object:
	# {
	# 	self._noteList: [ChordNote Objects],
	# 	self._intervalType: [IntervalTypes],
	# 	self._exactOffset: float,
	# 	self._exactEndTime: float,
	# 	self._measureNo: int,
	# 	self._intervalNo: int,
	# 	self._recognizedResultDict: {Tonic: ([TotalMatch chordname], [ExactMatch chordname, PossibleMatch chordname])}
	# 	self._equivalentGroupDict: {GroupNo: [(chordname, chordType, inversion, roman, chordFunction, tonic, groupNo)]}
	# }

	class IntervalType(object):
		# Simulate ENUM object
		# enum IntervalType {
		# 	Onbeat,
		# 	AfterBeat,
		# 	Continuous,
		# 	Normal,
		# 	ChangedBaseline,
		# }
		OnBeat, AfterBeat, Continuous, Normal, ChangedBaseline = range(5)
		@staticmethod
		def toString(intervalType=0):
			strList = ['OnBeat', 'AfterBeat', 'Continuous', 'Normal', 'ChangedBaseline']
			return strList[intervalType]

	def __init__(self, noteList=[], intervalNo=None, offset=None, endTime=None):
		self._noteList = list(noteList)
		self._intervalType = [self.IntervalType.Normal]
		if len(self._noteList):
			self._exactOffset = offset
			self._exactEndTime = endTime
			self._measureNo = self._noteList[0].measure
			self._intervalNo = intervalNo
		else:
			self._exactOffset = None
			self._exactEndTime = None
			self._measureNo = None
			self._intervalNo = None
		self._recognizedResultDict = {}
		self._equivalentGroupDict = {}

	@property
	def noteList(self):
		return self._noteList

	@property
	def measureNo(self):
		return self._measureNo

	@property
	def intervalNo(self):
		return self._intervalNo

	@property
	def exactOffset(self):
		return self._exactOffset

	@property
	def exactEndTime(self):
		return self._exactEndTime

	@property
	def intervalType(self):
		return self._intervalType

	# Result Dictionary from chord recognizer
	# {tonic: ([totalmatch, ...], [exactmatch, ...], [possiblematch, ... )}
	#
	# totalmatch / exactmatch / possiblematch structure: tuple of (cname, chordType, inversion, roman, tonic, groupNo)
	@property
	def recognizedResultDict(self):
		return self._recognizedResultDict

	# Equivalent Chord Group Dictionary
	# {groupNo: [(cname, chordType, inversion, roman, chordFunction, tonic, groupNo), ...]}
	# priority: TotalMatch -> ExactMatch -> PossibleMatch
	@property
	def equivalentGroupDict(self):
		return self._equivalentGroupDict

	# Funtion for printing debug message
	def debug(self):
		print "Measure: ", self._measureNo, " Interval: ", self._intervalNo
		print "\tStart at ", self._exactOffset, "End at ", self._exactEndTime

		typeStr = "\tType: "
		if self._intervalType[0] == self.IntervalType.Continuous:
			typeStr += "Continuous "
		else:
			if self._intervalType[0] == self.IntervalType.OnBeat:
				typeStr += "OnBeat "
			elif self._intervalType[0] == self.IntervalType.AfterBeat:
				typeStr += "AfterBeat "
			elif self._intervalType[0] == self.IntervalType.Normal:
				typeStr += "Normal "
			if len(self._intervalType) == 2 and self._intervalType[1] == self.IntervalType.ChangedBaseline:
				typeStr += "ChangedBaseline"
		print typeStr
		print ""

		noteStrList = [chordNote.debugMessage() for chordNote in self._noteList]
		print "\tNote List: ", noteStrList
		print ""

		result = self._recognizedResultDict

		# first print exact match
		print "\tTotal match chords are: "
		for tonic in result.keys():
			if len(result[tonic][0]) > 0:
				cnameList = [tup[0] for tup in result[tonic][0]]
				print "\t", tonic, ": ", cnameList
		print ""
		# first print exact match
		print "\tExact match chords are: "
		for tonic in result.keys():
			if len(result[tonic][1]) > 0:
				cnameList = [tup[0] for tup in result[tonic][1]]
				print "\t", tonic, ": ", cnameList
		print ""

		# then print possible match
		print "\tPossible match chords are: "
		for tonic in result.keys():
			if len(result[tonic][2]) > 0:
				cnameList = [tup[0] for tup in result[tonic][2]]
				print "\t", tonic, ": ", cnameList
		print ""

		print "\tEquivalent Chord: "
		for groupNo in self._equivalentGroupDict.keys():
			strList = [str(tup[5]+' '+tup[0]) for tup in self._equivalentGroupDict[groupNo]]
			print "\t", groupNo, ": ", strList
		print ""

	# never used
	def addNote(self, chordNote=None):
		if chordNote is not None:
			self._noteList.append(chordNote)

	# never used
	def replaceNote(self, originalNote=None, newNote=None):
		if originalNote is not None and newNote is not None:
			try:
				replaceIndex = self._noteList.index(originalNote)
				self._noteList.remove(originalNote)
				self._noteList.insert(replaceIndex, newNote)
			except ValueError:
				self._noteList.append(newNote)

	# return the ChordNote object in self._noteList that has the lowest frequency
	def getLowestFrequency(self):
		if len(self._noteList):
			return min([note.frequency for note in self._noteList])
		else:
			return None

	# transform ChordNote object list to specific format for the recognize function in ChordAnalyzingTool
	def getChordRecognizerInputFormat(self):
		inputDict = {}
		for chordNote in self._noteList:
			inputDict[chordNote.name] = chordNote.frequency
		return inputDict

	def setExactEndTime(self, endTime=None):
		self._exactEndTime = endTime

	def setIntervalType(self, intervalType=None):
		if len(self._intervalType) == 0:
			if intervalType is not self.IntervalType.ChangedBaseline:
				self.intervalType = [intervalType]
			else:
				self.intervalType = [self.IntervalType.Normal, self._intervalType.ChangedBaseline]
		else:
			if intervalType is self.IntervalType.ChangedBaseline:
				if len(self._intervalType) == 1:
					if self._intervalType[0] is not self.IntervalType.Continuous:
						self._intervalType.append(self.IntervalType.ChangedBaseline)
			else:
				self._intervalType[0] = intervalType

	def resetIntervalType(self):
		self._intervalType = [self.IntervalType.Normal]

	def setRecognizedResultDict(self, d={}):
		self._recognizedResultDict = d

	# function for analyze equivalentChord, generating self._equivalentGroupDict
	def analyzeEquivalentChord(self):
		resultDict = self._recognizedResultDict
		groupDict = {}
		groupCounter = 0
		for tonic in resultDict.keys():
			#total
			for i, item in enumerate(resultDict[tonic][0]):
				if groupCounter == 0:
					newTuple = (item[0], item[1], item[2], item[3], item[4], item[5], groupCounter)
					groupDict[groupCounter] = [newTuple]
					self._recognizedResultDict[tonic][0][i] = newTuple
					groupCounter += 1
				else:
					for groupNo in groupDict.keys():
						if self.__chkEquivalent(item, groupDict[groupNo][0]):
							newTuple = (item[0], item[1], item[2], item[3], item[4], item[5], groupNo)
							groupDict[groupNo].append(newTuple)
							self._recognizedResultDict[tonic][0][i] = newTuple
							item = self._recognizedResultDict[tonic][0][i]
							break
					if item[6] is None:
						newTuple = (item[0], item[1], item[2], item[3], item[4], item[5], groupCounter)
						groupDict[groupCounter] = [newTuple]
						self._recognizedResultDict[tonic][0][i] = newTuple
						groupCounter += 1
			#exact
			for i, item in enumerate(resultDict[tonic][1]):
				if groupCounter == 0:
					newTuple = (item[0], item[1], item[2], item[3], item[4], item[5], groupCounter)
					groupDict[groupCounter] = [newTuple]
					self._recognizedResultDict[tonic][1][i] = newTuple
					groupCounter += 1
				else:
					for groupNo in groupDict.keys():
						if self.__chkEquivalent(item, groupDict[groupNo][0]):
							newTuple = (item[0], item[1], item[2], item[3], item[4], item[5], groupNo)
							groupDict[groupNo].append(newTuple)
							self._recognizedResultDict[tonic][1][i] = newTuple
							item = self._recognizedResultDict[tonic][1][i]
							break
					if item[6] is None:
						newTuple = (item[0], item[1], item[2], item[3], item[4], item[5], groupCounter)
						groupDict[groupCounter] = [newTuple]
						self._recognizedResultDict[tonic][1][i] = newTuple
						groupCounter += 1
			#possible
			for i, item in enumerate(resultDict[tonic][2]):
				if groupCounter == 0:
					newTuple = (item[0], item[1], item[2], item[3], item[4], item[5], groupCounter)
					groupDict[groupCounter] = [newTuple]
					self._recognizedResultDict[tonic][2][i] = newTuple
					groupCounter += 1
				else:
					for groupNo in groupDict.keys():
						if self.__chkEquivalent(item, groupDict[groupNo][0]):
							newTuple = (item[0], item[1], item[2], item[3], item[4], item[5], groupNo)
							groupDict[groupNo].append(newTuple)
							self._recognizedResultDict[tonic][2][i] = newTuple
							item = self._recognizedResultDict[tonic][2][i]
							break
					if item[6] is None:
						newTuple = (item[0], item[1], item[2], item[3], item[4], item[5], groupCounter)
						groupDict[groupCounter] = [newTuple]
						self._recognizedResultDict[tonic][2][i] = newTuple
						groupCounter += 1
		self._equivalentGroupDict = groupDict

	# hardcoded function for checking equivalent chord
	def __chkEquivalent(self, targetChord, compareChord):
		noteDict = {
			'C':1, 'C#':2, 'Db':2,
			'D':3, 'D#':4, 'Eb':4, 'E':5, 'F':6,
			'F#':7, 'Gb':7, 'G':8, 'G#':9, 'Ab':9,
			'A':10, 'A#':11, 'Bb':11, 'B':12, 'Cb':12
		}
		romanDict = {
			'I':1,
			'bII':2, 'II':3,
			'bIII':4, 'III':5,
			'IV':6,
			'V':8,
			'bVI':9, 'VI':10,
			'bVII':11, 'VII':12
		}
		if targetChord[5][-1] == 'm':
			targetTonic = targetChord[5][:-1]
		else:
			targetTonic = targetChord[5]
		if compareChord[5][-1] == 'm':
			compareTonic = compareChord[5][:-1]
		else:
			compareTonic = compareChord[5]

		targetSum = (noteDict[targetTonic] + romanDict[targetChord[3]])%12
		compareSum = (noteDict[compareTonic] + romanDict[compareChord[3]])%12

		if not targetChord[1] == compareChord[1]:
			return False
		if not targetSum == compareSum:
			return False
		return True
