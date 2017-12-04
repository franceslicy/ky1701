import sys
import const

if len(sys.argv)!=3: exit()

input_key = sys.argv[1]
input_scale = sys.argv[2]

def get_output(in_key, in_scale):
    output = ""
    if input_scale.upper() == "MAJOR":
        scale = const.MAJOR
    else:
        scale = const.MINOR

    note = const.Note.parseFromString(input_key)
    output = output + note.printNote() + " "
    for i in scale[:-1]:
        note = note.noteAfterInterval([1, i])
        output = output + note.printNote() + " "
    return output

print(get_output(input_key, input_scale))