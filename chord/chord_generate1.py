from pprint import *
major_chord = {
	"I": ["C","E","G"],
	"I 7": ["C","E","G","B"],
	"II b": ["Db","F","Ab"],
	"II": ["D","F","A"],
	"II 7": ["D","F","A","C"],
	"III": ["E","G","B"],
	"III 7": ["E","G","B","D"],
	"IV": ["F","A","C"],
	"IV 7": ["F","A","C","E"],
	"V": ["G","B","D"],
	"V 7": ["G","B","D","F"],
	"VI b": ["Ab","C","Eb"],
	"VI Ger": ["Ab","C","Eb","F#"],
	"VI Fre": ["Ab","C","D","F#"],
	"VI Ita": ["Ab","C","F#"],
	"VI": ["A","C","E"],
	"VI 7": ["A","C","E","G"],
	"VII": ["B","D","F"],
	"VII 7": ["B","D","F","A"],
	"VII dim7": ["B","D","F","Ab"],
}

new_dict = {};
for key, chord in major_chord.items():
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