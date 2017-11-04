from pprint import *
minor_chord = {
	"I": ["C","Eb","G"],
	"I +": ["C", "E", "G"],
	"II b": ["Db","F","Ab"],
	"II": ["D","F","Ab"],
	"II 7": ["D","F","Ab","C"],
	"III": ["Eb","G","Bb"],
	"IV": ["F","Ab","C"],
	"IV +": ["F","A","C"],
	"V": ["G","Bb","D"],
	"V +": ["G","B","D"],
	"V +7": ["G","B","D","F"],
	"VI b": ["Ab","C","Eb"],
	"VI Ger": ["Ab","C","Eb","F#"],
	"VI Fre": ["Ab","C","D","F#"],
	"VI Ita": ["Ab","C","F#"],
	"VII": ["Bb","D","F"],
	"VII dim": ["B","D","F"],
	"VII dim7": ["B","D","F","Ab"],
}

new_dict = {};
for key, chord in minor_chord.items():
	if len(chord) == 4:
		if key == "VI Ger":
			new_dict[key] = [
				[chord[0],chord[1],chord[2],chord[3]],
				[chord[0],chord[2],chord[3]],
				[chord[1],chord[2],chord[3]],
				[chord[2],chord[3]],
			]
			continue
		if key == "VI Fre":
			new_dict[key] = [
				[chord[0],chord[1],chord[2],chord[3]],
				[chord[0],chord[1],chord[2]],
				[chord[0],chord[2],chord[3]],
				[chord[1],chord[2],chord[3]],
				[chord[0],chord[2]],
				[chord[1],chord[2]],
				[chord[2],chord[3]],
			]
			continue
		new_dict[key] = [
			[chord[0],chord[1],chord[2],chord[3]],
			# [chord[0],chord[1],chord[2]],
			[chord[0],chord[1],chord[3]],
			[chord[0],chord[2],chord[3]],
			[chord[1],chord[2],chord[3]],
			# [chord[0],chord[1]],
			[chord[0],chord[3]],
			[chord[1],chord[3]],
			[chord[2],chord[3]],
		]
	if len(chord) == 3:
		if key == "VI Ita":
			new_dict[key] = [
				[chord[0],chord[1],chord[2]],
				[chord[0],chord[2]],
				[chord[1],chord[2]],
			]
			continue
		new_dict[key] = [
			[chord[0],chord[1],chord[2]],
			[chord[0],chord[1]],
			[chord[0],chord[2]],
			[chord[1],chord[2]],
		]
pprint(new_dict)