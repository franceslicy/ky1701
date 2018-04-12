from ChordInterval import ChordInterval
from ProgressionBank import ProgressionBank
from ChordAnalyzingTool import ChordAnalyzingTool
import copy

class ProgressionVerifier(object):

	class ProgressionIntervalChoice(object):
		# Simulate ENUM object
		# enum ProgressionIntervalChoice {
		# 	Onbeat,
		# 	AllIntervalType,
		# 	ChangedBaseline
		# }

		# OnBeat					-	Select OnBeat Interval

		# AllIntervalType 			-	Select Interval of all IntervalType except Continuous

		# ChangedBaseline			-	Select ChangedBaseline Interval

		# the above mode are mutually exclusive, mode for choosing progression interval

		OnBeat, AllIntervalType, ChangedBaseline = range(3)

		_intervalTypeListDictionary = {
			OnBeat: [ChordInterval.IntervalType.OnBeat],
			AllIntervalType: [ChordInterval.IntervalType.OnBeat, ChordInterval.IntervalType.AfterBeat, ChordInterval.IntervalType.ChangedBaseline, ChordInterval.IntervalType.Normal],
			ChangedBaseline: [ChordInterval.IntervalType.ChangedBaseline]
		}

		@classmethod
		def toString(self, choice):
			cList = ['OnBeat', 'AllIntervalType', 'ChangedBaseline']
			return cList[choice]

		@classmethod
		def getChoiceList(self):
			return [self.OnBeat, self.AllIntervalType, self.ChangedBaseline]

		@classmethod
		def getTargetIntervalTypeList(self, choice):
			if choice in self._intervalTypeListDictionary:
				return self._intervalTypeListDictionary[choice]
			else:
				return []

	#simulate enum
	class ProgressionFeature(object):

		# enum ProgressionFeature {
		# 	VtoIProgression,
		# 	ChordFunction,
		# 	FirstComeFirstServe
		# }

		# VtoIProgression		-	Using the V - I progression as FIRST PRIORITY

		# ChordFunction			-	Using the chord function of each match tuple to prioritise the priority of progression, IN SECOND PRIORITY

		# FirstComeFirstServe	-	For selected interval type, simply find a nearest progression in same tonic, IN SECOND PRIORITY

		# ChordFunction and FirstComeFirstServe are mutually exclusive
		
		VtoIProgression, ChordFunction, FirstComeFirstServe = range(3)
		@classmethod
		def toString(self, feature):
			fList = ['VtoIProgression', 'ChordFunction', 'FirstComeFirstServe']
			return fList[feature]

		@classmethod
		def getFeatureList(self):
			return [self.VtoIProgression, self.ChordFunction, self.FirstComeFirstServe]

	def __init__(self, inputList=[], keyList=[]):
		self._inputList = copy.deepcopy(inputList)
		self._keyList = keyList
		self._pBank = ProgressionBank()
		self._analyzingTool = ChordAnalyzingTool()
		while len(self._inputList[-1]) == 0:
			self._inputList.pop()
		choiceList = self.ProgressionIntervalChoice.getChoiceList()
		self._invalidResult = {}

		# self._invalidResult is a dictionary to store the invalid recursion starting point throughout the progression process, the structure will be
		# {intervalChoice: {featureListString: {barLimit: {interval: [matchTuple, ... ]}}}}


	def verify(self, choice, featureList=[], barLimit=2):

		# init
		resultList = []
		featureList.sort();


		# get the invalidResultDictionary in current settings
		invalidResult = self.__getInvalidDictionary(choice=choice, featureList=featureList, barLimit=barLimit)

		# handle feature list
		if len(featureList) == 0:
			#default feature
			featureList.append(self.ProgressionFeature.VtoIProgression)
			featureList.append(self.ProgressionFeature.ChordFunction)
		if self.ProgressionFeature.ChordFunction in featureList and self.ProgressionFeature.FirstComeFirstServe in featureList:
			#remove ChordFunction to use FirstComeFirstServe as default
			featureList.remove(self.ProgressionFeature.FirstComeFirstServe)

		if self.ProgressionFeature.ChordFunction not in featureList and self.ProgressionFeature.FirstComeFirstServe not in featureList:
			# if both not selected, use ChordFunction as default
			featureList.append(self.ProgressionFeature.ChordFunction)


		# find starting point interval
		targetTypeList = self.ProgressionIntervalChoice.getTargetIntervalTypeList(choice)
		startingPointIntervalList = []
		touchEnd = False
		measureCnt = 0
		while len(startingPointIntervalList) == 0 and not touchEnd:
			(startingPointIntervalList, touchEnd) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=measureCnt, startInterval=0, barLimit=barLimit)
			measureCnt += barLimit
		# for interval in startingPointIntervalList:
		# 	interval.debug()
		# 	print ""
		if len(startingPointIntervalList) == 0:
			print "Could not find starting point in current mode: "+self.ProgressionIntervalChoice.toString(choice)
		else:
			startingPoint = startingPointIntervalList[0]
			matchTupleRomanIndex = self._analyzingTool.convertMatchTupleKeyToIndex('roman')
			matchTupleTonicIndex = self._analyzingTool.convertMatchTupleKeyToIndex('tonic')
			referencedKeyList = []
			for key in self._keyList:
				referencedKey = key.tonic.name
				if key.mode == 'minor':
					referencedKey += 'm'
				referencedKeyList.append(referencedKey)
			matchTuplePriorityList = []
			allMatches = self.__getOrderedMatchesDict(interval=startingPoint, totalMatch=True, exactMatch=True, possibleMatch=True)
			for referencedKey in referencedKeyList:
				for key in sorted(allMatches.keys()):
					matchTuplePriorityList += [matchTuple for matchTuple in allMatches[key] if matchTuple not in matchTuplePriorityList and matchTuple[matchTupleTonicIndex] == referencedKey and matchTuple[matchTupleRomanIndex] == 'I' or matchTuple[matchTupleRomanIndex] == 'V']
			for key in sorted(allMatches.keys()):
				matchTuplePriorityList += [matchTuple for matchTuple in allMatches[key] if matchTuple not in matchTuplePriorityList and (matchTuple[matchTupleRomanIndex] == 'I' or matchTuple[matchTupleRomanIndex] == 'V')]
			for key in sorted(allMatches.keys()):
				matchTuplePriorityList += [matchTuple for matchTuple in allMatches[key] if matchTuple not in matchTuplePriorityList]
			# print "Starting Point Priority List: "
			# for matchTuple in matchTuplePriorityList:
			# 	print matchTuple
			# print ""
			# start progression
			for matchTuple in matchTuplePriorityList:
				if startingPoint in invalidResult and matchTuple in invalidResult[startingPoint]:
					continue
				recursiveResult = self.__recursiveProgression(startingInterval=startingPoint, startingMatch=matchTuple, choice=choice, featureList=featureList, barLimit=barLimit, previousNotSubdominant=None)
				if len(recursiveResult) == 0:
					if startingPoint not in invalidResult:
						invalidResult[startingPoint] = []
					invalidResult[startingPoint].append(matchTuple)
				else:
					resultList = recursiveResult
					break
		return resultList


	def __recursiveProgression(self, startingInterval, startingMatch, choice, featureList, barLimit, previousNotSubdominant):

		# get the invalidResultDictionary in current settings
		invalidResult = self.__getInvalidDictionary(choice=choice, featureList=featureList, barLimit=barLimit)


		intervalA = startingInterval
		matchTupleA = startingMatch
		if previousNotSubdominant is not None:
			(intervalP, (cnameP, chordTypeP, inversionP, romanP, chordFunctionP, tonicP, groupNoP)) = previousNotSubdominant
		(cnameA, chordTypeA, inverionA, romanA, chordFunctionA, tonicA, groupNoA) = matchTupleA

		targetTypeList = self.ProgressionIntervalChoice.getTargetIntervalTypeList(choice)
		matchTupleRomanIndex = self._analyzingTool.convertMatchTupleKeyToIndex('roman')
		matchTupleTonicIndex = self._analyzingTool.convertMatchTupleKeyToIndex('tonic')
		matchTupleCNameIndex = self._analyzingTool.convertMatchTupleKeyToIndex('cname')
		matchTupleChordFunctionIndex = self._analyzingTool.convertMatchTupleKeyToIndex('chordFunction')

		# check if current interval is the last PriorInterval, if no, progressionBarLimit=2, if yes, progressionBarLimit=3
		(targetIntervalWithinThisBar, touchEnd) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=intervalA.measureNo, startInterval=intervalA.intervalNo+1, barLimit=1)
		if touchEnd and len(targetIntervalWithinThisBar) == 0:
			return [(intervalA, matchTupleA)]
		if len(targetIntervalWithinThisBar) == 0:
			progressionBarLimitA = barLimit+1
		else:
			progressionBarLimitA = barLimit

		# here is the first module, VtoIProgression
		if self.ProgressionFeature.VtoIProgression in featureList:
			if choice == self.ProgressionIntervalChoice.ChangedBaseline:
				# special case for changedBaseline IntervalChoice, only select the first interval
				(targetIntervalWithinBarLimitA, touchEndA) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=intervalA.measureNo, startInterval=intervalA.intervalNo+1, barLimit=0)
			else:
				(targetIntervalWithinBarLimitA, touchEndA) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=intervalA.measureNo, startInterval=intervalA.intervalNo+1, barLimit=progressionBarLimitA/2)
			for i, intervalB in enumerate(targetIntervalWithinBarLimitA):

				totalExactMatches = self.__getOrderedMatchesDict(interval=intervalB, totalMatch=True, exactMatch=True, possibleMatch=False)
				intervalBRomanVList = []
				for key in sorted(totalExactMatches.keys()):
					intervalBRomanVList += [matchTuple for matchTuple in totalExactMatches[key] if matchTuple[matchTupleRomanIndex] == 'V' and matchTuple[matchTupleTonicIndex][0] != tonicA[0]]

				# check if current interval is the last PriorInterval, if no, progressionBarLimit=2, if yes, progressionBarLimit=2
				if i+1 < len(targetIntervalWithinBarLimitA) and targetIntervalWithinBarLimitA[i+1].measureNo == intervalB.measureNo:
					progressionBarLimitB = barLimit
				else:
					progressionBarLimitB = barLimit+1
				if choice == self.ProgressionIntervalChoice.ChangedBaseline:
					# special case for changedBaseline IntervalChoice, only select the first interval
					(targetIntervalWithinBarLimitB, touchEndB) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=intervalB.measureNo, startInterval=intervalB.intervalNo+1, barLimit=0)
				else:
					(targetIntervalWithinBarLimitB, touchEndB) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=intervalB.measureNo, startInterval=intervalB.intervalNo+1, barLimit=progressionBarLimitB/2)
				for matchTupleB in intervalBRomanVList:
					(cnameB, chordTypeB, inverionB, romanB, chordFunctionB, tonicB, groupNoB) = matchTupleB
					for j, intervalC in enumerate(targetIntervalWithinBarLimitB):

						allMatches = self.__getOrderedMatchesDict(interval=intervalC, totalMatch=True, exactMatch=True, possibleMatch=True)
						sameTonicRomanIList = []
						for key in sorted(allMatches.keys()):
							sameTonicRomanIList += [matchTuple for matchTuple in allMatches[key] if (matchTuple[matchTupleRomanIndex] == 'I' and matchTuple[matchTupleTonicIndex] == tonicB)]
						for matchTupleC in sameTonicRomanIList:
							(cnameC, chordTypeC, inversionC, romanC, chordFunctionC, tonicC, groupNoC) = matchTupleC
							if self.__isPerfectCadenceProgression(previousChordType=chordTypeB, afterChordType=chordTypeC):

								# examine intervalA to intervalC first
								eqvIntervalCinTonicA = [matchTuple for matchTuple in intervalC.equivalentGroupDict[groupNoC] if matchTuple[matchTupleTonicIndex] == matchTupleA[matchTupleTonicIndex]]
								if len(eqvIntervalCinTonicA):
									beforeCName = matchTupleA[matchTupleCNameIndex]
									afterCName = eqvIntervalCinTonicA[0][matchTupleCNameIndex]
									if matchTupleA[matchTupleTonicIndex][-1] == 'm':
										verifyFunction = self._pBank.verifyMinor
									else:
										verifyFunction = self._pBank.verifyMajor
									if verifyFunction(before=beforeCName, after=afterCName) == "Yes" or beforeCName == afterCName:

										if not(intervalC in invalidResult and eqvIntervalCinTonicA[0] in invalidResult[intervalC]):

											if chordFunctionA != "Subdominant":
												newPreviousNotSubdominant = (intervalA, matchTupleA)
											else:
												newPreviousNotSubdominant = previousNotSubdominant

											# next progression with no tonic changed
											recursiveResult = self.__recursiveProgression(startingInterval=intervalC, startingMatch=eqvIntervalCinTonicA[0], choice=choice, featureList=featureList, barLimit=barLimit, previousNotSubdominant=newPreviousNotSubdominant)

											if len(recursiveResult) == 0:
												if intervalC not in invalidResult:
													invalidResult[intervalC] = []
												invalidResult[intervalC].append(eqvIntervalCinTonicA[0])
											else:
												return [(intervalA, matchTupleA), (intervalB, matchTupleB)] + recursiveResult

								# examine intervalA to intervalB
								eqvIntervalBinTonicA = [matchTuple for matchTuple in intervalB.equivalentGroupDict[groupNoB] if matchTuple[matchTupleTonicIndex] == matchTupleA[matchTupleTonicIndex]]
								if len(eqvIntervalBinTonicA):
									beforeCName = matchTupleA[matchTupleCNameIndex]
									afterCName = eqvIntervalBinTonicA[0][matchTupleCNameIndex]
									if matchTupleA[matchTupleTonicIndex][-1] == 'm':
										verifyFunction = self._pBank.verifyMinor
									else:
										verifyFunction = self._pBank.verifyMajor
									if verifyFunction(before=beforeCName, after=afterCName) == "Yes" or beforeCName == afterCName:

										if not(intervalC in invalidResult and matchTupleC in invalidResult[intervalC]):

											if chordFunctionB != "Subdominant":
												newPreviousNotSubdominant = (intervalB, matchTupleB)
											else:
												newPreviousNotSubdominant = previousNotSubdominant

											# next progression with tonic changed
											recursiveResult = self.__recursiveProgression(startingInterval=intervalC, startingMatch=matchTupleC, choice=choice, featureList=featureList, barLimit=barLimit, previousNotSubdominant=newPreviousNotSubdominant)

											if len(recursiveResult) == 0:
												if intervalC not in invalidResult:
													invalidResult[intervalC] = []
												invalidResult[intervalC].append(matchTupleC)
											else:
												return [(intervalA, matchTupleA), (intervalB, matchTupleB)] + recursiveResult
		# second feature, prioritise using chord function
		if self.ProgressionFeature.ChordFunction in featureList:
			if choice == self.ProgressionIntervalChoice.ChangedBaseline:
				(targetIntervalWithinBarLimitA, touchEndA) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=intervalA.measureNo, startInterval=intervalA.intervalNo+1, barLimit=0)
			else:
				(targetIntervalWithinBarLimitA, touchEnd) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=intervalA.measureNo, startInterval=intervalA.intervalNo+1, barLimit=progressionBarLimitA)

			# first search for remaining unchanged
			farestUnchangedChordFunction = None
			for i, intervalB in enumerate(targetIntervalWithinBarLimitA):
				allMatches = self.__getOrderedMatchesDict(interval=intervalB, totalMatch=True, exactMatch=True, possibleMatch=True)
				allMatchesList = []
				for key in sorted(allMatches.keys()):
					allMatchesList += [matchTuple for matchTuple in allMatches[key]]
				unchangedList = [matchTuple for matchTuple in allMatchesList if matchTuple[matchTupleTonicIndex] == tonicA and matchTuple[matchTupleCNameIndex] == cnameA]
				if len(unchangedList):
					farestUnchangedChordFunction = (intervalB, unchangedList[0])
				else:
					break
			if farestUnchangedChordFunction is not None:
				# success in searching for unchanged chord function interval
				(intervalB, matchTupleB) = farestUnchangedChordFunction
				if not(intervalB in invalidResult and matchTupleB in invalidResult[intervalB]):

					if chordFunctionA != "Subdominant":
						newPreviousNotSubdominant = (intervalA, matchTupleA)
					else:
						newPreviousNotSubdominant = previousNotSubdominant

					#next progression with chord function remain unchanged
					recursiveResult = self.__recursiveProgression(startingInterval=intervalB, startingMatch=matchTupleB, choice=choice, featureList=featureList, barLimit=barLimit, previousNotSubdominant=newPreviousNotSubdominant)

					if len(recursiveResult) == 0:
						if intervalB not in invalidResult:
							invalidResult[intervalB] = []
						invalidResult[intervalB].append(matchTupleB)
					else:
						return [(intervalA, matchTupleA)] + recursiveResult

			# then make a priority list base on different chord function of matchTupleA

			# separate following operation in different bars, but with the limit of barLimit
			for bar in range(progressionBarLimitA):
				startMeasure = intervalA.measureNo + bar
				if bar == 0:
					startInterval = intervalA.intervalNo + 1
				else:
					startInterval = 0
				if choice == self.ProgressionIntervalChoice.ChangedBaseline:
					(targetIntervalWithinBarLimitA, touchEndA) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=intervalA.measureNo, startInterval=intervalA.intervalNo+1, barLimit=0)
				else:
					(targetIntervalWithinBarLimitA, touchEndA) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=startMeasure, startInterval=startInterval, barLimit=1)
				unrankedPriorityListDict = {'Tonic': [], 'Dominant': [], 'Subdominant': [], 'Undefined': []}
				priorityList = []
				for intervalB in targetIntervalWithinBarLimitA:
					allMatches = self.__getOrderedMatchesDict(interval=intervalB, totalMatch=True, exactMatch=True, possibleMatch=True)
					sameTonicList = []
					for key in sorted(allMatches.keys()):
						sameTonicList += [matchTuple for matchTuple in allMatches[key] if matchTuple[matchTupleTonicIndex] == tonicA]

					# In any case, Subdominant will be the first priority
					priorityList += [(intervalB, matchTupleB) for matchTupleB in sameTonicList if matchTupleB[matchTupleChordFunctionIndex] == "Subdominant"]

					if chordFunctionA == "Dominant" or (previousNotSubdominant is None and chordFunctionA == "Subdominant") or (previousNotSubdominant is not None and chordFunctionA == "Subdominant" and chordFunctionP == "Dominant"):
						# for Dominant, Tonic ranked higher than Dominant
						priorityList += [(intervalB, matchTupleB) for matchTupleB in sameTonicList if matchTupleB[matchTupleChordFunctionIndex] == "Tonic"]

						# save to the dictionary and append later
						unrankedPriorityListDict['Dominant'] += [(intervalB, matchTupleB) for matchTupleB in sameTonicList if matchTupleB[matchTupleChordFunctionIndex] == "Dominant"]

					elif chordFunctionA == "Tonic" or (previousNotSubdominant is not None and chordFunctionA == "Subdominant" and chordFunctionP == "Tonic"):
						# for Tonic, Dominant ranked higher than Tonic
						priorityList += [(intervalB, matchTupleB) for matchTupleB in sameTonicList if matchTupleB[matchTupleChordFunctionIndex] == "Dominant"]

						# save to the dictionary and append later
						unrankedPriorityListDict['Tonic'] += [(intervalB, matchTupleB) for matchTupleB in sameTonicList if matchTupleB[matchTupleChordFunctionIndex] == "Tonic"]

					# save to the dictionary and append later
					unrankedPriorityListDict['Undefined'] += [(intervalB, matchTupleB) for matchTupleB in sameTonicList if matchTupleB[matchTupleChordFunctionIndex] == "Undefined"]

				# append the less priority list
				if chordFunctionA == "Dominant" or (previousNotSubdominant is None and chordFunctionA == "Subdominant") or (previousNotSubdominant is not None and chordFunctionA == "Subdominant" and chordFunctionP == "Dominant"):
					priorityList += unrankedPriorityListDict['Dominant']
				elif chordFunctionA == "Tonic" or (previousNotSubdominant is not None and chordFunctionA == "Subdominant" and chordFunctionP == "Tonic"):
					priorityList += unrankedPriorityListDict['Tonic']
				priorityList += unrankedPriorityListDict['Undefined']

				# printPriorityList = [str(intervalB.measureNo)+'_'+str(intervalB.intervalNo)+'_'+str(matchTupleB[0])+'_'+str(matchTupleB[4]) for (intervalB, matchTupleB) in priorityList]
				# print "At Measure: ", intervalA.measureNo, " Interval: ", intervalA.intervalNo, " priorityList: ", printPriorityList
				for (intervalB, matchTupleB) in priorityList:
					beforeCName = cnameA
					afterCName = matchTupleB[matchTupleCNameIndex]
					if tonicA[-1] == 'm':
						verifyFunction = self._pBank.verifyMinor
					else:
						verifyFunction = self._pBank.verifyMajor
					if verifyFunction(before=beforeCName, after=afterCName) == "Yes" or beforeCName == afterCName:
						if intervalB in invalidResult and matchTupleB in invalidResult[intervalB]:
							continue

						if chordFunctionA != "Subdominant":
							newPreviousNotSubdominant = (intervalA, matchTupleA)
						else:
							newPreviousNotSubdominant = previousNotSubdominant

						recursiveResult = self.__recursiveProgression(startingInterval=intervalB, startingMatch=matchTupleB, choice=choice, featureList=featureList, barLimit=barLimit, previousNotSubdominant=newPreviousNotSubdominant)

						if len(recursiveResult) == 0:
							if intervalB not in invalidResult:
								invalidResult[intervalB] = []
							invalidResult[intervalB].append(matchTupleB)
						else:

							return [(intervalA, matchTupleA)] + recursiveResult
				if choice == self.ProgressionIntervalChoice.ChangedBaseline:
					break

		# Third Feature, first come first serve
		elif self.ProgressionFeature.FirstComeFirstServe in featureList:
			# no result above, now first come first serve, with selected interval type
			if choice == self.ProgressionIntervalChoice.ChangedBaseline:
				# special case for changedBaseline IntervalChoice, only select the first interval
				(targetIntervalWithinBarLimitA, touchEndA) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=intervalA.measureNo, startInterval=intervalA.intervalNo+1, barLimit=0)
			else:
				(targetIntervalWithinBarLimitA, touchEndA) = self.__findAllIntervalByIntervalTypeWithLimit(targetIntervalType=targetTypeList, startMeasure=intervalA.measureNo, startInterval=intervalA.intervalNo+1, barLimit=progressionBarLimitA)
			for i, intervalB in enumerate(targetIntervalWithinBarLimitA):
				allMatches = self.__getOrderedMatchesDict(interval=intervalB, totalMatch=True, exactMatch=True, possibleMatch=True)
				sameTonicList = []
				for key in sorted(allMatches.keys()):
					sameTonicList += [matchTuple for matchTuple in allMatches[key] if matchTuple[matchTupleTonicIndex] == tonicA ]
				for matchTupleB in sameTonicList:
					beforeCName = cnameA
					afterCName = matchTupleB[matchTupleCNameIndex]
					if tonicA[-1] == 'm':
						verifyFunction = self._pBank.verifyMinor
					else:
						verifyFunction = self._pBank.verifyMajor
					if verifyFunction(before=beforeCName, after=afterCName) == "Yes" or beforeCName == afterCName:

						if intervalB in invalidResult and matchTupleB in invalidResult[intervalB]:
							continue

						if chordFunctionA != "Subdominant":
							newPreviousNotSubdominant = (intervalA, matchTupleA)
						else:
							newPreviousNotSubdominant = previousNotSubdominant

						# next progression
						recursiveResult = self.__recursiveProgression(startingInterval=intervalB, startingMatch=matchTupleB, choice=choice, featureList=featureList, barLimit=barLimit, previousNotSubdominant=newPreviousNotSubdominant)

						if len(recursiveResult) == 0:
							if intervalB not in invalidResult:
								invalidResult[intervalB] = []
							invalidResult[intervalB].append(matchTupleB)
						else:
							return [(intervalA, matchTupleA)] + recursiveResult
		return []


	def __getInvalidDictionary(self, choice, featureList, barLimit):
		if choice not in self._invalidResult:
			self._invalidResult[choice] = {}

		featureListString = ""
		for feature in featureList:
			featureListString += self.ProgressionFeature.toString(feature)
		if featureListString not in self._invalidResult[choice]:
			self._invalidResult[choice][featureListString] = {}

		if barLimit not in self._invalidResult[choice][featureListString]:
			self._invalidResult[choice][featureListString][barLimit] = {}

		return self._invalidResult[choice][featureListString][barLimit]


	def __isPerfectCadenceProgression(self, previousChordType, afterChordType):
		V7toI = previousChordType == "Dominant 7th" and afterChordType == "Major"
		VtoI = previousChordType == "Major" and afterChordType == "Major"
		vtoi = previousChordType == "Minor" and afterChordType == "Minor"
		return V7toI or VtoI or vtoi


	def __getOrderedMatchesDict(self, interval, totalMatch=True, exactMatch=True, possibleMatch=True):
		orderedMatchesDict = {}
		totalMatchList = []
		exactMatchList = []
		possibleMatchList = []
		for tonic in interval.recognizedResultDict.keys():
			totalMatchList += [match for match in interval.recognizedResultDict[tonic][0]]
			exactMatchList += [match for match in interval.recognizedResultDict[tonic][1]]
			possibleMatchList += [match for match in interval.recognizedResultDict[tonic][2]]
		if totalMatch:
			orderedMatchesDict['1-totalMatch'] = totalMatchList
		if exactMatch:
			orderedMatchesDict['2-exactMatch'] = exactMatchList
		if possibleMatch:
			orderedMatchesDict['3-possibleMatch'] = possibleMatchList
		return orderedMatchesDict


	def __findAllIntervalByIntervalTypeWithLimit(self, targetIntervalType, startMeasure, startInterval, barLimit):
		intervalList = []
		if barLimit == 0:
			# special case, select the next five possible target interval neglecting bar limit,
			touchEnd = False
			while not touchEnd:
				(intervalInOneBar, touchEnd) = self.__findAllIntervalWithLimit(startMeasure=startMeasure, startInterval=startInterval, barLimit=1)
				for interval in intervalInOneBar:
					for intervalType in interval.intervalType:
						if intervalType in targetIntervalType:
							intervalList.append(interval)
							if len(intervalList) == 5 or touchEnd:
								return (intervalList, touchEnd)
				startMeasure += 1
				startInterval = 0
		else:
			(allIntervalWithLimit, touchEnd) = self.__findAllIntervalWithLimit(startMeasure=startMeasure, startInterval=startInterval, barLimit=barLimit)
			for interval in allIntervalWithLimit:
				for intervalType in interval.intervalType:
					if intervalType in targetIntervalType:
						intervalList.append(interval)
						break
		return (intervalList, touchEnd)


	def __findAllIntervalWithLimit(self, startMeasure, startInterval, barLimit):

		touchEnd = False
		if startMeasure + barLimit >= len(self._inputList):
			limit = len(self._inputList)
			touchEnd = True
		else:
			limit = startMeasure + barLimit

		intervalList = []
		for measureIndex in range(startMeasure, limit):
			for interval in self._inputList[measureIndex]:
				if measureIndex == startMeasure and interval.intervalNo < startInterval:
					continue
				intervalList.append(interval)
		return (intervalList, touchEnd)
