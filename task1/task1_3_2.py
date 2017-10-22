import sys
import const
import subprocess
import itertools

def getNotes(key, scale, chord_num):
    output = subprocess.check_output(["python", "task1_2.py", key, scale, chord_num]).decode('utf-8').strip()
    return frozenset(output.split(' '))


input_key = sys.argv[1]
input_notes = sys.argv[2:]

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

order_table = {
    'C': 0, 0:'C',
    'D': 1, 1:'D',
    'E': 2, 2:'E',
    'F': 3, 3:'F',
    'G': 4, 4:'G',
    'A': 5, 5:'A',
    'B': 6, 6:'B'
}

#In cases of total match and inclusion
found = 0
notes_set = frozenset(input_notes)
if(len(notes_set)<=3):
    for notes in major_table:
        if notes_set < notes:
            print(input_key + " " + "Major Chord " + major_table[notes] + " (Inclusion)")
            found = 1
        elif notes_set == notes:
            print(input_key + " " + "Major Chord " + major_table[notes] + " (Total Match)")
            found = 1
    for notes in minor_table:
        if notes_set < notes:
            print(input_key + " " + "Minor Chord " + minor_table[notes] + " (Inclusion)")
            found = 1
        elif notes_set == notes:
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

tmplist = input_notes
orderlist = [order_table[x] for x in tmplist]
minNote = order_table[min(orderlist)]
tmplist = list(filter((minNote).__ne__, tmplist))

for i in range(len(tmplist)):
    new_notes = []
    for j in range(len(tmplist)):
        if(i!=j): new_notes.append(tmplist[j])
    new_notes.append(minNote)
    new_notes = frozenset(set(new_notes))
    if(len(new_notes)>3): continue
    for notes in major_table:
        if new_notes <= notes:
            chord_num = major_table[notes]
            if(major_found[chord_num]==0):
                print(input_key + " " + "Major Chord " + chord_num + " (One Mismatch)")
                major_found[chord_num] = 1
            found = 1
    for notes in minor_table:
        if new_notes <= notes:
            chord_num = minor_table[notes]
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

tmplist = input_notes
orderlist = [order_table[x] for x in tmplist]
minNote = order_table[min(orderlist)]
tmplist = list(filter((minNote).__ne__, tmplist))

if(len(tmplist)<=2): sys.exit()
subsets = itertools.combinations(tmplist, len(tmplist)-2)
for subset in subsets:
    new_notes = list(subset)
    new_notes.append(minNote)
    new_notes = frozenset(new_notes)
    for notes in major_table:
        if new_notes <= notes:
            chord_num = major_table[notes]
            if(major_found[chord_num]==0):
                print(input_key + " " + "Major Chord " + chord_num + " (Two Mismatches)")
                major_found[chord_num] = 1
            found = 1
    for notes in minor_table:
        if new_notes <= notes:
            chord_num = minor_table[notes]
            if(minor_found[chord_num]==0):
                print(input_key + " " + "Minor Chord " + chord_num + " (Two Mismatches)")
                minor_found[chord_num] = 1
            found = 1

if(found==0):
    print("No possible match for given notes")