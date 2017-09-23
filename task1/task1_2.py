import sys
import const

if len(sys.argv)!=4: exit()

input_key = sys.argv[1]
input_scale = sys.argv[2]
input_chord = sys.argv[3].upper()
output = ""

chord_number = const.ROMAN.index(input_chord)
note = const.Note.parseFromString(input_key)
if input_scale.upper() == "MAJOR":
	root_interval = sum(const.MAJOR[:chord_number])
	chord_name = const.chord_major[input_chord]
else:
	root_interval = sum(const.MINOR[:chord_number])
	chord_name = const.chord_minor[input_chord]

# root note
note = note.noteAfterInterval([chord_number, root_interval])
print(note.printNote(), end=" ")

chord = const.chord_type[chord_name]

for interval in chord:
	note = note.noteAfterInterval(interval)
	print(note.printNote(), end=" ")
print()