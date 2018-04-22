from music21 import *
from copy import deepcopy
import const

class Triad:
	"""docstring for Triad"""
	def __init__(self, triadType, rank, inversion=None, rootName=None, nNameIn=None, nNameList=None):
		self.triadType = triadType
		self.missingIndex = self.getMissingNoteIndex(rank)
		self.rootName = rootName or self.genRootName(nNameIn, inversion)
		self.nNameList = deepcopy(nNameList) or self.genCompleteNameList(deepcopy(nNameIn))
		# self.haveBassNote = (bassNoteName in self.nNameList)
		# self.totalOccurance = totalOccurance

	def __eq__(self,other):
		return self.triadType == other.triadType and self.rootName == other.rootName

	def __hash__(self):
		return hash((self.triadType, self.rootName))

	def __repr__(self):
		return ("<{} {}>".format(self.__class__.__name__, self.getPrintNotation()))

	# only called at __init__
	def genRootName(self, nNameList, inversion):
		if self.missingIndex == None: # perfect match
			if inversion == 0:
				root = nNameList[0]
			elif inversion == 1:
				root = nNameList[2]
			elif inversion == 2:
				root = nNameList[1]
		elif self.missingIndex == 1 or self.missingIndex == 2:
			root = nNameList[inversion]
		elif self.missingIndex == 0:
			third = nNameList[inversion]
			triad = next(t for t in const.TRIADS if t[0]==self.triadType)
			interval_roodThird = triad[1][1][0]
			root = interval_roodThird.reverse().transposePitch(pitch.Pitch(third)).name
		return root

	# only called at __init__
	def genCompleteNameList(self, nNameList):
		if self.missingIndex == None: return nNameList
		triad = next(t for t in const.TRIADS if t[0]==self.triadType)
		if self.missingIndex == 2:
			interval_roodFifth = triad[1][2][0]
			fifth = interval_roodFifth.transposePitch(pitch.Pitch(self.rootName)).name
			nNameList.append(fifth)
		if self.missingIndex == 1:
			interval_roodThird = triad[1][1][0]
			third = interval_roodThird.transposePitch(pitch.Pitch(self.rootName)).name
			nNameList.append(third)
		if self.missingIndex == 0:
			nNameList.append(self.rootName)
		return sorted(nNameList)

	def isSame(self, triad_2):
		return self.triadType == triad_2.triadType and self.rootName == triad_2.rootName

	def isNoteNameInTriad(self, nName):
		return nName in self.nNameList

	def isPerfectMatch(self):
		return self.missingIndex == None

	def is7thChord(self):
		return len(self.nNameList) == 4

	def getMissingPriority(self):
		if self.missingIndex == None: return 3
		if self.missingIndex == 2: return 2
		if self.missingIndex == 1: return 1
		if self.missingIndex == 0: return 0

	def getPrintNotation(self):
		return self.rootName+self.triadType

	@staticmethod
	def getMissingNoteIndex(rank):
		if rank == 0: return None
		if rank == 1: return 2		# fifth note
		if rank == 2: return 1		# third note
		if rank == 3: return 0		# root note

	@staticmethod
	def sortNoteName(nList):
		nList = sorted(nList)


	@classmethod
	def getPossibleTriad(cls, nList):
		def nNameIndex(n):
			index = ord(n[0]) if n[0] >= 'C' else ord(n[0])+7
			index = index + (len(n)-1)*((-0.1 if n[1]=='-' else 0.1) if len(n)>=2 else 0)
			return index

		nList = sorted(nList, key=lambda n:nNameIndex(n))
		note_intervals = [interval.Interval(note.Note(nList[i]), note.Note(nList[i+1])) for i in range(len(nList)-1)]
		if len(nList) == 3:
			for triad in const.TRIADS:
				triadType = triad[0]
				triad_interval_list = triad[1][0]
				for i in range(len(triad_interval_list)-1):
					if note_intervals == triad_interval_list[i:i+2]:
						return cls(triadType, rank=0, inversion=i, nNameIn=nList)
			return None
		elif len(nList) == 2:
			possibleTriads = []
			for triad in const.TRIADS:
				triadType = triad[0]
				triad_interval_lists = triad[1][1:]
				for rank, triad_interval_list in enumerate(triad_interval_lists):
					for i in range(len(triad_interval_list)):
						if note_intervals[0] == triad_interval_list[i]:
							possibleTriads.append(cls(triadType, rank=rank+1, inversion=i, nNameIn=nList))
			return possibleTriads

	@classmethod
	def mergeChord(cls, triad_1, triad_2):
		if triad_1.isSame(triad_2):		#same chord, update missing index
			if triad_1.missingIndex != triad_2.missingIndex:
				triad_1.missingIndex = None 			# all chord notes included in either chord
			return triad_1
		elif triad_1.is7thChord() != triad_2.is7thChord():	#only either one is 7th
			if triad_1.is7thChord() and set(triad_2.nNameList).issubset(set(triad_1.nNameList)):		#triad_1 is 7th
				chord_7th = triad_1
				chord_triad = triad_2
			elif triad_2.is7thChord() and set(triad_1.nNameList).issubset(set(triad_2.nNameList)):		# triad_2 is 7th
				chord_7th = triad_2
				chord_triad = triad_1
			else: return False

			if chord_7th.rootName == chord_triad.rootName:		# same root chords
				if chord_7th.missingIndex != chord_triad.missingIndex:
					chord_7th.missingIndex = None
			else:
				if ((chord_7th.missingIndex != chord_triad.missingIndex+1) if chord_triad.missingIndex is not None else True):
					chord_7th.missingIndex = None
			return chord_7th
		return False

	@classmethod
	def mergeTo7th(cls, triad_1, triad_2):
		if triad_1.isSame(triad_2): return False
		if len(set(triad_1.nNameList).intersection(set(triad_2.nNameList))) != 2: return False
		interval_roots = interval.Interval(pitch.Pitch(triad_1.rootName), pitch.Pitch(triad_2.rootName))
		if interval_roots.directedName[-2:] == '-3' or (interval_roots.directedName[-1] == '6' and interval_roots.directedName[-2] != '-'):		#triad_2 is root
			triad_root = triad_2
			triad_third = triad_1
		elif interval_roots.directedName[-1] == '3' or interval_roots.directedName[-2:] == '-6':	#triad_1 is root
			triad_root = triad_1
			triad_third = triad_2
		else: return False

		if triad_root.missingIndex == 0 or triad_third.missingIndex == 2: return False		# not having root or 7th note
		chordType7th = next((s[0] for s in const.SEVENTHS if s[1]==[triad_root.triadType, triad_third.triadType]),None)
		if chordType7th:
			triadType = chordType7th
		else:
			return False
		nNameList = sorted(list(set(triad_root.nNameList).union(set(triad_third.nNameList))))
		missingIndex = triad_root.missingIndex
		if ((triad_root.missingIndex != triad_third.missingIndex+1) if triad_third.missingIndex is not None else True):
			missingIndex = None
		return cls(triadType, missingIndex, rootName=triad_root.rootName, nNameList=nNameList)