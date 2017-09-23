LETTERS = ["C", "D", "E", "F", "G", "A", "B"]
ACCIDENTAL = {-2:'bb', -1:'b', 0:'', 1:'#', 2:'##'}
INTEVAL = [2, 2, 1, 2, 2, 2, 1]

MAJOR = [2, 2, 1, 2, 2, 2, 1]
MINOR = [2, 1, 2, 2, 1, 2, 2]

# perfect_unison = [0, 0] perf1
# minor_second = [1, 1] min2
# major_second = [1, 2] maj2
# minor_third = [2, 3] min3
# major_third = [2, 4] maj3
# perfect_fourth = [3, 5] perf4
# augmented_fourth = [3, 6] aug4
# diminished_fifth = [4, 6] dim5
# perfect_fifth = [4, 7] perf5
# augmented_fifth = [4, 8] aug5
# minor_sixth = [5, 8] min6
# major_sixth = [5, 9] maj6
# augmented_sixth = [5, 10] aug6
# diminished_seventh = [6, 9] dim7
# minor_seventh = [6, 10] min7
# major_seventh = [6, 11] maj7
# perfect_octave = [7, 12] perf8

perf1 = [0, 0] 
min2 = [1, 1] 
maj2 = [1, 2] 
min3 = [2, 3] 
maj3 = [2, 4] 
perf4 = [3, 5] 
aug4 = [3, 6] 
dim5 = [4, 6] 
perf5 = [4, 7] 
aug5 = [4, 8] 
min6 = [5, 8] 
maj6 = [5, 9] 
aug6 = [5, 10] 
dim7 = [6, 9] 
min7 = [6, 10] 
maj7 = [6, 11] 
perf8 = [7, 12] 

chord_type = {
	"major_triad": [maj3, min3, perf4],
	"minor_triad": [min3, maj3, perf4],
	"diminished_triad": [min3, min3, aug4]
}

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']

chord_major = {
	'I': "major_triad", 
	'II': "minor_triad",
	'III': "minor_triad",
	'IV': "major_triad",
	'V': "major_triad",
	'VI': "minor_triad",
	'VII': "diminished_triad"
}

chord_minor = {
	'I': "minor_triad", 
	'II': "diminished_triad",
	'III': "major_triad",
	'IV': "minor_triad",
	'V': "minor_triad",
	'VI': "major_triad",
	'VII': "major_triad"
}


def nextNIndex(length, start, n):
	return (start+n)%length

class Note:
	@classmethod
	def parseFromString(cls, string):
		letter = string[0].upper()
		if letter not in LETTERS:
			raise ValueError('invalid letter or accidental')
		if len(string) > 1:
			accidental = string[1:]
		else:
			accidental = ''
		if accidental not in ACCIDENTAL.values():
			raise ValueError('invalid letter or accidental')
		note = cls(LETTERS.index(letter), next(k for k,v in ACCIDENTAL.items() if v==accidental))
		return note

	def __init__(self, letter, accidental):
		if letter<0 or letter>=len(LETTERS):
			raise ValueError('invalid letter or accidental')
		self.letter = letter
		if abs(accidental) > 2:
			raise ValueError('invalid letter or accidental')
		self.accidental = accidental

	def printNote(self):
		return LETTERS[self.letter]+ACCIDENTAL[self.accidental]

	def noteAfterInterval(self, interval):
		natural_step = interval[0]
		half_step = interval[1]
		# check how many half step for natural step
		letter = self.letter
		LETTERS_len = len(LETTERS)
		total_half_step = -(self.accidental)
		for i in range(natural_step):
			total_half_step += INTEVAL[letter]
			letter = nextNIndex(LETTERS_len, letter, 1)
		accidental = half_step - total_half_step
		if abs(accidental) > 2:
			raise ValueError('invalid letter or accidental')
		return Note(letter, accidental)