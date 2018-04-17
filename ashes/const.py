from music21 import *
# vaild traids
i_M3 = interval.Interval('M3')
i_m3 = interval.Interval('m3')
i_d3 = interval.Interval('d3')
i_P4 = interval.Interval('P4')
i_A4 = interval.Interval('A4')
i_d4 = interval.Interval('d4')
i_P5 = interval.Interval('P5')
i_A5 = interval.Interval('A5')
i_d5 = interval.Interval('d5')
i_M6 = interval.Interval('M6')
i_m6 = interval.Interval('m6')
i_A6 = interval.Interval('A6')

TRIADS = [
	("Maj", [[i_M3, i_m3, i_P4, i_M3], [i_M3, i_m6], [i_P5, i_P4], [i_m3, i_M6]]),
	("min", [[i_m3, i_M3, i_P4, i_m3], [i_m3, i_M6], [i_P5, i_P4], [i_M3, i_m6]]),
	("dim", [[i_m3, i_m3, i_A4, i_m3], [i_m3, i_M6], [i_d5, i_A4], [i_m3, i_M6]]),
	("Aug", [[i_M3, i_M3, i_d4, i_M3], [i_M3, i_m6], [i_A5, i_d4], [i_M3, i_m6]]),
	("It6", [[i_d3, i_M3, i_A4, i_d3], [i_d3, i_A6], [i_d5, i_A4], [i_M3, i_m6]]),
]
SEVENTHS = [
	("Maj7", ["Maj", "min"]),
	("min7", ["min", "Maj"]),
	("7", ["Maj", "dim"]),
	("dim7", ["dim", "dim"]),
	("min7b5", ["dim", "min"]),
]