import sys
import const

if len(sys.argv)!=3: exit()

input_key = sys.argv[1]
input_scale = sys.argv[2]
output = ""
if input_scale.upper() == "MAJOR":
	scale = const.MAJOR
else:
	scale = const.MINOR

note = const.Note.parseFromString(input_key)
print(note.printNote(), end=" ")
for i in scale:
	note = note.noteAfterInterval([1, i])
	print(note.printNote(), end=" ")
print()