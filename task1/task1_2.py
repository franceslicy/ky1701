import sys
import const

if len(sys.argv)!=4: exit()

input_key = sys.argv[1]
input_scale = sys.argv[2]
input_chord = sys.argv[3].upper()

def get_output(in_key, in_scale, in_chord):
    output = ""
    chord_number = const.ROMAN.index(in_chord)
    note = const.Note.parseFromString(in_key)
    if in_scale.upper() == "MAJOR":
        root_interval = sum(const.MAJOR[:chord_number])
        chord_name = const.chord_major[in_chord]
    else:
        root_interval = sum(const.MINOR[:chord_number])
        chord_name = const.chord_minor[in_chord]

    # root note
    note = note.noteAfterInterval([chord_number, root_interval])
    output = output + note.printNote() + " "

    chord = const.chord_type[chord_name]

    for interval in chord[:-1]:
        note = note.noteAfterInterval(interval)
        output = output + note.printNote() + " "
    return output

print(get_output(input_key, input_scale, input_chord))