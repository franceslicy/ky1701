from ChordAnalyzingTool import ChordAnalyzingTool
from ProgressionVerifier import ProgressionVerifier
from ChordNote import ChordNote
from ChordInterval import ChordInterval
import music21
import copy
import os
import cPickle

class Identifier(object):

	StoragePath = "./Storage/"

	# Identifier Object:
	# {
	# 	self._score: Music21.Score,
	# 	self._scoreFilename: String,
	# 	self._chordifiedScore: Music21.Score,
	# 	self._analyzingTool: ChordAnalyzingTool,
	# 	self._keyList: [Music21.Key],
	# 	self._preparedScoreInput: [[ChordInterval],[ChordInterval], ... ],
	#	self._progressionVerifier: ProgressionVerifier
	# }

	#_preparedScoreInput structure
	#[measure 1, measure 2, [ interval 1, interval 2, interval Object, interval 4, ... ], measure 4, ... ]
	#                       ^                         ^
	#                   in measure 3            in interval 3

	def __init__(self, score, scoreFilename):
		self._score = score
		self._scoreFilename = scoreFilename
		self._chordifiedScore = score.chordify()

		#initialize chord analyzing tool object
		self._analyzingTool = ChordAnalyzingTool()

		# traverse through whole score to extract notes and create interval objects
		scoreInput = self.__readScore(score=self._chordifiedScore)

		# run basic chord analyzing algorithm
		self.__basicAnalyze(inputs=scoreInput)

		# store prepared score
		self._preparedScoreInput = scoreInput

		# extract the key object list for priority control in progression
		self._keyList = [key for key in self._chordifiedScore.recurse().getElementsByClass(music21.key.Key)]
		if not len(self._keyList):
			self._keyList = [key for key in self._chordifiedScore.recurse().getElementsByClass(music21.key.KeySignature)]
			if len(self._keyList):
				self._keyList += [self._keyList[0].asKey('major')]
				self._keyList += [self._keyList[0].asKey('minor')]
				self._keyList.remove(self._keyList[0])

		# initialize progression verifier
		self._progressionVerifier = ProgressionVerifier(inputList=self._preparedScoreInput, keyList=self._keyList)

	@classmethod
	def getIdentifier(self, score, scoreFilename):
		# first search for saved storage
		print "Searching storage folder for saved ChordIdentifier"
		identifier = self.__load(scoreFilename=scoreFilename)

		if not identifier:
			print "Initializing new ChordIdentifier"
			identifier = Identifier(score=score, scoreFilename=scoreFilename)
			print "Save into storage folder"
			identifier.save(overwrite=True)
		return identifier

	@classmethod
	def __searchInStorage(self, scoreFilename):
		filePath = os.getcwd()+'/'+self.StoragePath+scoreFilename+'.ChordIdentifier'
		if os.path.isfile(filePath):
			return filePath
		else:
			return None

	@classmethod
	def __load(self, scoreFilename):
		filePath = self.__searchInStorage(scoreFilename)
		if filePath:
			return cPickle.load(open(filePath, "r"))
		else:
			print "Unable to find saved ChordIdentifier."
			return None

	def save(self, overwrite=False):
		filePath = self.__searchInStorage(self._scoreFilename)
		if filePath and overwrite:
			cPickle.dump(self, open(filePath, "w"), True)
		elif not filePath:
			filePath = os.getcwd()+'/'+self.StoragePath+self._scoreFilename+'.ChordIdentifier'
			cPickle.dump(self, open(filePath, "w"), True)

	def printPreparedScore(self):
		inputs = self._preparedScoreInput
		for measure in inputs:
			for interval in measure:
				interval.debug()
				print ""

	# Driving function for running progression for this Identifier
	# If verbal = true, print out result,
	# If output = true, save output in xml format with used features and interval type as default filename
	# If outputFilename specified, save output in xml format with specified file name
	# specify target interval type by setting "choice"
	# specify features by setting "featureList"
	# specify progression bar limit by setting "barLimit"
	def runProgression(self, choice, featureList=[], barLimit=2, verbal=False, output=False, outputFilename=None):
		result = self._progressionVerifier.verify(choice=choice, featureList=featureList, barLimit=barLimit)
		if verbal:
			cnameIndex = self._analyzingTool.convertMatchTupleKeyToIndex(key='cname')
			tonicIndex = self._analyzingTool.convertMatchTupleKeyToIndex(key='tonic')
			for (interval, matchTuple) in result:
				string = "At Measure "+str(interval.measureNo)+", offset "+str(interval.exactOffset)+", "
				string += str(matchTuple[tonicIndex])+str(matchTuple[cnameIndex])+", "+str(matchTuple)
				print string
		if output:
			if not outputFilename:
				outputFilename = ''.join(self._scoreFilename.split('.xml')[:-1]) + '_'
				outputFilename += ProgressionVerifier.ProgressionIntervalChoice.toString(choice) + '_'
				outputFilename += '_'.join([ProgressionVerifier.ProgressionFeature.toString(f) for f in featureList]) + '_'
				outputFilename += str(barLimit)+'bar' + '.xml'
			self.__outputResultInMusicXml(result=result, outputFilename=outputFilename)
		return result

	def __outputResultInMusicXml(self, result, outputFilename):
		cnameIndex = self._analyzingTool.convertMatchTupleKeyToIndex(key='cname')
		tonicIndex = self._analyzingTool.convertMatchTupleKeyToIndex(key='tonic')
		score = copy.deepcopy(self._score)
		copiedChordifiedScore = copy.deepcopy(self._chordifiedScore)
		for c in copiedChordifiedScore.recurse().getElementsByClass(music21.chord.Chord):
			c.closedPosition(forceOctave=5, inPlace=True)

		for (interval, matchTuple) in result:
			c = [offsetMap.element for offsetMap in copiedChordifiedScore.measure(interval.measureNo+1).offsetMap() if isinstance(offsetMap.element, music21.chord.Chord) and offsetMap.offset == interval.exactOffset]
			if len(c):
				c[0].addLyric(str(matchTuple[tonicIndex])+str(matchTuple[cnameIndex]))
		score.insert(0, copiedChordifiedScore)
		score.write('musicxml', fp=os.getcwd()+'/'+outputFilename)

	def __basicAnalyze(self, inputs):
		for i, measure in enumerate(inputs):
			for j, interval in enumerate(measure):
				tonicResult = self._analyzingTool.recognizeByAllTonic(interval)
				inputs[i][j].setRecognizedResultDict(tonicResult)
				inputs[i][j].analyzeEquivalentChord()

	def __readScore(self, score):
		inputs = []
		count = 1
		currentTimeSignature = None
		currentBaseLineFreq = None
		measure = score.measure(count)
		while measure is not None:
			if measure.timeSignature is not None:
				currentTimeSignature = measure.timeSignature
			if currentTimeSignature is None:
				# print "Error - No time signature detected."
				break
			#operation in each bar
			inputIntervalList = []
			continuousInterval = None
			intervalCounter = 0
			for offsetMap in measure.offsetMap():
				chordNoteList = []
				element = offsetMap.element
				if isinstance(element, music21.chord.Chord):
					for pitch in element.pitches:
						chordNoteList.append(ChordNote(name=pitch.name,frequency=pitch.frequency,offset=offsetMap.offset,endTime=offsetMap.endTime,measure=count-1))
				if len(chordNoteList) == 1:
					if continuousInterval is not None:
						noteNameList = [chordNote.name for chordNote in continuousInterval.noteList]
						if chordNoteList[0].name in noteNameList:
							for chordNote in continuousInterval.noteList:
								if chordNoteList[0].name == chordNote.name and chordNoteList[0].frequency < chordNote.frequency:
									continuousInterval.replaceNote(chordNote, chordNoteList[0])
									break
						else:
							continuousInterval.addNote(chordNoteList[0])
					else:
						continuousInterval = ChordInterval(intervalNo=intervalCounter, noteList=list(chordNoteList), offset=chordNoteList[0].offset)
						continuousInterval.setIntervalType(ChordInterval.IntervalType.Continuous)
						intervalCounter += 1
				elif len(chordNoteList):
					if continuousInterval is not None:
						inputIntervalList.append(continuousInterval)
						continuousInterval = None
						inputIntervalList[-1].setExactEndTime(inputIntervalList[-1].noteList[-1].endTime)
					noteNameList = [chordNote.name for chordNote in chordNoteList]
					tmpChordNoteDict = {}
					for chordNote in chordNoteList:
						if chordNote.name not in tmpChordNoteDict:
							tmpChordNoteDict[chordNote.name] = chordNote
						elif chordNote.frequency < tmpChordNoteDict[chordNote.name].frequency:
							tmpChordNoteDict[chordNote.name] = chordNote
					inputIntervalList.append(ChordInterval(intervalNo=intervalCounter, noteList=list(tmpChordNoteDict.values()), offset=chordNoteList[0].offset, endTime=chordNoteList[0].endTime))

					# check previous interval that whether it is OnBeat Interval
					if len(inputIntervalList) > 1 and inputIntervalList[-2].intervalType == ChordInterval.IntervalType.OnBeat:
						inputIntervalList[-1].setIntervalType(ChordInterval.IntervalType.AfterBeat)

					beatDuration = currentTimeSignature.beatDuration.quarterLength
					# check current interval that whether it is OnBeat
					if inputIntervalList[-1].exactOffset / beatDuration % 1 == 0:
						inputIntervalList[-1].setIntervalType(ChordInterval.IntervalType.OnBeat)
					# default will be Normal type

					# now check did baseline changed, only applicable to OnBeat / AfterBeat / Normal
					lowestFreq = inputIntervalList[-1].getLowestFrequency()
					if not (lowestFreq == currentBaseLineFreq):
						inputIntervalList[-1].setIntervalType(ChordInterval.IntervalType.ChangedBaseline)
						currentBaseLineFreq = lowestFreq

					intervalCounter += 1

			# continuousInterval can consist only the notes within the same measure, so handle the unhandled continuous notes here
			if continuousInterval is not None:
				inputIntervalList.append(continuousInterval)
				continuousInterval = None
				inputIntervalList[-1].setExactEndTime(inputIntervalList[-1].noteList[-1].endTime)
			inputs.append(inputIntervalList)

			count += 1
			measure = score.measure(count)
		return inputs
