from music21 import *
import numpy as np
from copy import deepcopy
from collections import Counter
from itertools import combinations
from triad import *

class Ashes:
	"""docstring for Ashes"""

	def __init__(self, m):
		self.measure = m.voicesToParts()
		for n in self.measure.recurse().getElementsByClass('GeneralNote'):
			if n.duration.isGrace:
				self.measure.remove(n, recurse=True)
		# remove invalid part
		for p in self.measure.parts:
			if not p.duration == self.measure.duration: self.measure.remove(p)
		self.measure = figuredBass.checker.getVoiceLeadingMoments(self.measure)
		# make grid
		self.beat = [n.beat for n in self.measure.parts[0].recurse().getElementsByClass('GeneralNote')]
		self.duration = [n.quarterLength for n in self.measure.parts[0].recurse().getElementsByClass('GeneralNote')]
		grid_array = [[n for n in p.recurse().getElementsByClass('GeneralNote')] for p in self.measure.parts]
		
		#remove rest parts & rests
		grid_array = [p for p in grid_array if any(not n.isRest for n in p)]
		if not grid_array: return
		self.grid = np.empty((len(grid_array),len(grid_array[0])), dtype=object)
		for i,p in enumerate(grid_array):
			current_n = None
			for j,n in enumerate(p):
				if n.isRest: 
					fill = current_n or next((x for x in p[j+1:] if not x.isRest), None)
					fill_duration = n.quarterLength
					n = deepcopy(fill) if fill else n
					n.quarterLength = fill_duration
				else:
					current_n = n
				self.grid[i,j] = n

		# get bass
		self.bassline = [min([(min(n,key=lambda x:x.pitch.midi) if n.isChord else n) for n in list(self.grid[:,j])], key=lambda x:x.pitch.midi).name for j in range(self.grid.shape[1])]
		#get pitch count
		self.pitchCount = [dict(Counter(sum([self.getnamesOfNote(n) for n in self.grid[:,j]],[]))) for j in range(self.grid.shape[1])]

	


	def lowestMovementPart(self):
		def haveSameName(n1,n2):
			n1 = [n1] if n1.isNote else n1
			n2 = [n2] if n2.isNote else n2
			for i in n1:
				for j in n2:
					if i.name == j.name: return True
			return False
		changeBeatOfParts = [[1] for i in range(self.grid.shape[0])]
		for i in range(self.grid.shape[0]):
			for j in range(self.grid.shape[1]-1):
				if not haveSameName(self.grid[i,j], self.grid[i,j+1]):
					changeBeatOfParts[i].append(self.beat[j+1])
		changeBeatCounts = [len(beats) for beats in changeBeatOfParts]
		lowestMovementParts = [i for i,count in enumerate(changeBeatCounts) if count == min(changeBeatCounts)]
		# print(changeBeatCounts,lowestMovementParts)
		if len(lowestMovementParts) > 1:
			#lowest sounding
			avgSoundings = [np.mean([(np.mean([cn.pitch.midi for cn in n]) if n.isChord else n.pitch.midi) for n in self.grid[i]]) for i in lowestMovementParts]
			lowestMovementPartIndex = lowestMovementParts[avgSoundings.index(min(avgSoundings))]
		else:
			lowestMovementPartIndex = lowestMovementParts[0]
		return (lowestMovementPartIndex, changeBeatOfParts[lowestMovementPartIndex])


	def verticalMatch(self):
		self.grid_possibleTriads = []
		for j in range(self.grid.shape[1]):
			pitchCount = self.pitchCount[j]
			if len(pitchCount) >= 3:
				possibleList = combinations(pitchCount.keys(),3)
				possibleTriads = [x for x in [Triad.getPossibleTriad(list(nList)) for nList in possibleList] if x]
				if not possibleTriads:
					possibleList = combinations(pitchCount.keys(),2)
					possibleTriads = [x for xs in [Triad.getPossibleTriad(list(nList)) for nList in possibleList] for x in xs if x]
			elif len(pitchCount) == 2:
				possibleTriads = Triad.getPossibleTriad(pitchCount.keys())
			else: possibleTriads = None
			self.grid_possibleTriads.append(possibleTriads)
		return self.grid_possibleTriads

	def verticalMerge(self):
		#merge if two perfect match
		for j, possibleTriads in enumerate(self.grid_possibleTriads):
			if possibleTriads:
				# merge 7th chord
				possibleTriadsMerge = combinations(possibleTriads,2)
				possibleTriads.extend([x for x in [Triad.mergeTo7th(triad[0],triad[1]) for triad in possibleTriadsMerge] if x])
			if possibleTriads and len(possibleTriads) > 1 and all([triad.isPerfectMatch() for triad in possibleTriads]):
				bestMerge = sorted([(self.getScoreTuple(j, triad, bass=True),triad) for triad in possibleTriads], key=lambda x:x[0], reverse=True)[0]
				self.grid_possibleTriads[j] = [bestMerge[1]]
				# self.grid_possibleTriads[j] = possibleTriads
		return self.grid_possibleTriads

	def horizontalMerge(self):
		self.cutoffBeat = self.lowestMovementPart()[1]
		round1_Triad = []
		accumulateTriad = []
		j_start = 0
		# first round merge: possible merge within cutoff
		for j, possibleTriads in enumerate(self.grid_possibleTriads):
			if not j_start == 0 and self.beat[j] in self.cutoffBeat:
				# push chord before
				round1_Triad.append((j_start, accumulateTriad))
				accumulateTriad = possibleTriads
				j_start = j
			if accumulateTriad and possibleTriads:
				currentTriad = list(set([x for x in [Triad.mergeChord(triad_1,triad_2) for triad_1 in accumulateTriad for triad_2 in possibleTriads] if x]))
				if not currentTriad and all(not x.isPerfectMatch() for x in possibleTriads):
					currentTriad.extend([x for x in accumulateTriad if x not in currentTriad and x.is7thChord() and len(set(self.pitchCount[j].keys()).union(set(x.nNameList))) >= 2])
				if currentTriad:
					accumulateTriad = currentTriad
				else:
					# cannot merge
					# push chord before, add cutoff
					round1_Triad.append((j_start, accumulateTriad))
					self.cutoffBeat.append(self.beat[j])
					accumulateTriad = possibleTriads
					j_start = j
			if not accumulateTriad:
				accumulateTriad = possibleTriads
		#push chord before
		round1_Triad.append((j_start, accumulateTriad))

		# second round merge: merge between cutoff
		self.grid_finalTriads = []
		accumulateTriad = []
		j_start = 0
		for (j, possibleTriads) in round1_Triad:
			if accumulateTriad and possibleTriads:
				currentTriad = list(set([x for x in [Triad.mergeChord(triad_1,triad_2) for triad_1 in accumulateTriad for triad_2 in possibleTriads] if x]))
				# print(j,currentTriad)
				if currentTriad:
					accumulateTriad = currentTriad
				else:
					bestMerge = self.getHorizontalBestMerge(accumulateTriad, j_start, j)
					self.grid_finalTriads.append((j_start, bestMerge))
					accumulateTriad = possibleTriads
					j_start = j
			if not accumulateTriad:
				accumulateTriad = possibleTriads
		bestMerge = self.getHorizontalBestMerge(accumulateTriad, j_start)
		self.grid_finalTriads.append((j_start, bestMerge))
		return self.grid_finalTriads

	def getChordinBeat(self):
		return {self.beat[j]:triad for (j,triad) in self.grid_finalTriads}

	def isValidMeasure(self):
		return hasattr(self, 'grid')

	def getHorizontalBestMerge(self, triadList, j_start, j_end=None):
		if not triadList: return None
		if len(triadList) == 1: return triadList[0]
		bestMerge = sorted([(self.getScoreTuple(j_start, triad, j_end=(j_end or self.grid.shape[1])),triad) for triad in triadList], key=lambda x:x[0], reverse=True)[0]
		return bestMerge[1]

	def getScoreTuple(self, j_start, triad, bass=None, j_end=None):
		totalOccurence = 0
		for j in range(j_start, j_end or j_start+1):
			pitchCount = self.pitchCount[j]
			duration = self.duration[j]
			totalOccurence = totalOccurence + sum([(pitchCount[pitchName]*duration if pitchName in pitchCount else 0) for pitchName in triad.nNameList])
		if bass:
			withBass = self.bassline[j_start] in triad.nNameList
			return (withBass, totalOccurence, triad.getMissingPriority())
		else:
			return (totalOccurence, triad.getMissingPriority())

	@staticmethod
	def getnamesOfNote(n):
		if n.isRest: return []
		if n.isChord: return [cn.name for cn in n]
		else: return [n.name]

	@staticmethod
	def getPitchesOfNote(n):
		if n.isRest: return []
		if n.isChord: return [cn.pitch for cn in n]
		else: return [n.pitch]

	@staticmethod
	def getPitchesNorIndexOfNote(n):
		if n.isRest: return []
		if n.isChord: return [cn.pitch.midi%12 for cn in n]
		else: return [n.pitch.midi%12]