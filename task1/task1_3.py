import sys
import const
import subprocess
import itertools

def getNotes(key, scale, chord_num):
    output = subprocess.check_output(["python", "task1_2.py", key, scale, chord_num]).decode('utf-8').strip()
    return frozenset(output.split(' '))


input_key = sys.argv[1]
input_notes = frozenset(sys.argv[2:])

if(len(input_notes)>5 or len(input_notes)==0):
    print("No possible match for given notes")
    exit()

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


#In cases of total match and inclusion
found = 0
if(len(input_notes)<=3):
    for notes in major_table:
        if input_notes < notes:
            print(input_key + " " + "Major Chord " + major_table[notes] + " (Inclusion)")
            found = 1
        elif input_notes == notes:
            print(input_key + " " + "Major Chord " + major_table[notes] + " (Total Match)")
            found = 1
    for notes in minor_table:
        if input_notes < notes:
            print(input_key + " " + "Minor Chord " + minor_table[notes] + " (Inclusion)")
            found = 1
        elif input_notes == notes:
            print(input_key + " " + "Minor Chord " + minor_table[notes] + " (Total Match)")
            found = 1
    if(found==1): print()

#In cases of one mismatch
major_found = {
    'I': 0,
    'II': 0,
    'III': 0,
    'IV': 0,
    'V': 0,
    'VI': 0,
    'VII': 0
}

minor_found = {
    'I': 0,
    'II': 0,
    'III': 0,
    'IV': 0,
    'V': 0,
    'VI': 0,
    'VII': 0
}
if(len(input_notes)>1):
    tmplist = [x for x in input_notes]
    for i in range(len(tmplist)):
        new_notes = []
        for j in range(len(tmplist)):
            if(i!=j): new_notes.append(tmplist[j])
        new_notes = frozenset(set(new_notes))
        for notes in major_table:
            if new_notes <= notes:
                chord_num = major_table[notes]
                if(major_found[chord_num]==0):
                    print(input_key + " " + "Major Chord " + chord_num + " (One Mismatch)")
                    major_found[chord_num] = 1
                found = 1
        for notes in minor_table:
            if new_notes <= notes:
                if(minor_found[chord_num]==0):
                    print(input_key + " " + "Minor Chord " + chord_num + " (One Mismatch)")
                    minor_found[chord_num] = 1
                found = 1
    if(found==1): print()

#In cases of two mismatches
major_found = {
    'I': 0,
    'II': 0,
    'III': 0,
    'IV': 0,
    'V': 0,
    'VI': 0,
    'VII': 0
}

minor_found = {
    'I': 0,
    'II': 0,
    'III': 0,
    'IV': 0,
    'V': 0,
    'VI': 0,
    'VII': 0
}
if(len(input_notes)>2):
    subsets = itertools.combinations(input_notes, len(input_notes)-2)
    for subset in subsets:
        new_notes = frozenset(subset)
        for notes in major_table:
            if new_notes <= notes:
                chord_num = major_table[notes]
                if(major_found[chord_num]==0):
                    print(input_key + " " + "Major Chord " + chord_num + " (Two Mismatches)")
                    major_found[chord_num] = 1
                found = 1
        for notes in minor_table:
            if new_notes <= notes:
                if(minor_found[chord_num]==0):
                    print(input_key + " " + "Minor Chord " + chord_num + " (Two Mismatches)")
                    minor_found[chord_num] = 1
                found = 1

if(found==0):
    print("No possible match for given notes")