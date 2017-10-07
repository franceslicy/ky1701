import sys
import const
import subprocess

def getNotes(key, scale, chord_num):
    output = subprocess.check_output(["python", "task1_2.py", key, scale, chord_num]).decode('utf-8').strip()
    return frozenset(output.split(' '))


input_key = sys.argv[1]
input_notes = frozenset(sys.argv[2:])

major_table = {
    getNotes(input_key, "major", "I"): 'I',
    getNotes(input_key, "major", "II"): 'II',
    getNotes(input_key, "major", "III"): 'III',
    getNotes(input_key, "major", "IV"): 'IV',
    getNotes(input_key, "major", "V"): 'V',
    getNotes(input_key, "major", "VI"): 'VI',
    getNotes(input_key, "major", "VII"): 'VII'
}

minor_table = {
    getNotes(input_key, "minor", "I"): 'I',
    getNotes(input_key, "minor", "II"): 'II',
    getNotes(input_key, "minor", "III"): 'III',
    getNotes(input_key, "minor", "IV"): 'IV',
    getNotes(input_key, "minor", "V"): 'V',
    getNotes(input_key, "minor", "VI"): 'VI',
    getNotes(input_key, "minor", "VII"): 'VII'
}


#In cases of total match
if(input_notes in major_table):
    print(input_key + " " + "Major Chord " + major_table[input_notes])
elif(input_notes in minor_table):
    print(input_key + " " + "Minor Chord " + minor_table[input_notes])
else:
    print("No possible match for gievn notes")