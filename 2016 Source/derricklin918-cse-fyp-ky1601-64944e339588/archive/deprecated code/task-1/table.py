from chordname import *

major_progression = [["I", Interval.perfect_unison],
                     ["bII" , Interval.minor_second],
                     ["II" , Interval.major_second],
                     ["II7", Interval.major_second],
                     ["III" , Interval.major_third],
                     ["IV" , Interval.perfect_fourth],
                     ["V" , Interval.perfect_fifth],
                     ["V7", Interval.perfect_fifth],
                     ["bVI" , Interval.minor_sixth],
                     ["gerVI" , Interval.minor_sixth],
                     ["freVI" , Interval.minor_sixth],
                     ["itaVI" , Interval.minor_sixth],
                     ["VI" , Interval.major_sixth],
                     ["VII" , Interval.major_seventh],
                     ["dimVII" , Interval.major_seventh]]

minor_progression = [["I", Interval.perfect_unison],
                     ["I+" , Interval.perfect_unison],
                     ["bII" , Interval.minor_second],
                     ["II" , Interval.major_second],
                     ["II7", Interval.major_second],
                     ["III" , Interval.minor_third],
                     ["IV" , Interval.perfect_fourth],
                     ["IV+" , Interval.perfect_fourth],
                     ["V", Interval.perfect_fifth],
                     ["V+", Interval.perfect_fifth],
                     ["V+7", Interval.perfect_fifth],
                     ["VI", Interval.minor_sixth],
                     ["gerVI" , Interval.minor_sixth],
                     ["freVI" , Interval.minor_sixth],
                     ["itaVI" , Interval.minor_sixth],
                     ["VII" , Interval.minor_seventh],
                     ["dimVII" , Interval.major_seventh]]

def print_table_from_key(key_name):

    if len(key_name) == 1:
        key_note = Note(Note.letter_to_pitch_number(key_name), key_name[0], 0)
    else:
        if key_name[1] == "b":
            key_note = Note(Note.letter_to_pitch_number(key_name), key_name[0], -1)
        elif key_name[1] == "#":
            key_note = Note(Note.letter_to_pitch_number(key_name), key_name[0], 1)


    with open("output_2.txt", "a") as text_file:
        print(key_note.get_note_name() + " major", file=text_file)
        for roman_number in major_progression:
            target_note = Note.get_interval_note(key_note, roman_number[1])
            chord = Chord.major_roman_number_to_chord(roman_number[0], target_note)
            print(roman_number[0] + ":", end="", file=text_file)
            chord.print_txt(text_file)

        print(file=text_file)
        print(key_note.get_note_name() + " minor", file=text_file)
        for roman_number in minor_progression:
            target_note = Note.get_interval_note(key_note, roman_number[1])
            chord = Chord.minor_roman_number_to_chord(roman_number[0], target_note)
            print(roman_number[0] + ":", end="", file=text_file)
            chord.print_txt(text_file)
        print(file=text_file)

key_list = ["C", "D", "E", "F", "G", "A", "B", "Db", "C#", "Eb", "D#", "Fb", "E#", "Gb", "F#", "Ab", "G#", "Bb", "A#", "Cb", "B#"]
for key in key_list:
    print_table_from_key(key)
