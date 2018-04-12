# CUHK CSE FYP 2016 Piano Reduction Task 1
# LIN Hang Yu AU Ho Wing
# Superviser: Prof. Kevin Yip
# Co-superviser: Prof. Lucas Wong

# Note class
class Note:
    """This class is a data structure for musical notes"""
    def __init__(self, pitch_number, base_note, accidental):
        """class constructor with three properties. pitch_number refers to a scale of 12 semitone (0 - 11)
           base_note contains a string that refers to the musical note without any accidentals(flat or sharp)
           accidental contains a number that refers to any accidentals that the notes have
        """
        self.__pitch_number = pitch_number
        # musical note without accidentals i,e. (C, D, E, F, G, A, B)
        self.__base_note = base_note
        # accidental in number form i.e. -2 = double flat -1 = flat 0 = neutral 1 = sharp 2 = double sharp
        self.__accidental = accidental

    @property
    def pitch_number(self):
        return self.__pitch_number

    @property
    def base_note(self):
        return self.__base_note

    @property
    def accidental(self):
        return self.__accidental

    @pitch_number.setter
    def pitch_number(self, value):
        self.__pitch_number = value

    @base_note.setter
    def base_note(self, value):
        self.__base_note = value


    @accidental.setter
    def accidental(self, value):
        self.__accidental = value

    def get_accidental_sign(self):
        """# get accidental sign"""
        options = {-2 : "bb",
                   -1 : "b",
                   0 : "",
                   1 : "#",
                   2 : "x"
                   }
        return options[self.__accidental]


    def print_note(self):
        """# print out the note"""
        number = self.pitch_number
        name = self.base_note
        accidental = self.get_accidental_sign()

        print("{}{} : {}".format(name, accidental, number))


    def get_note_name(self):
        """get the name of the note (with accidental sign)"""
        return self.base_note + self.get_accidental_sign()

    @classmethod
    def letter_to_pitch_number(cls, note):
        """class method to translate musical note to pitch number"""
        value = -1
        if note == "C" or note == "B#":
            value = 0
        elif note == "C#" or note == "Db":
            value = 1
        elif note == "D":
            value = 2
        elif note == "D#" or note == "Eb":
            value = 3
        elif note == "E" or note == "Fb":
            value = 4
        elif note == "F" or note == "E#":
            value = 5
        elif note == "F#" or note == "Gb":
            value = 6
        elif note == "G":
            value = 7
        elif note == "G#" or note =="Ab":
            value = 8
        elif note == "A":
            value = 9
        elif note == "A#" or  note =="Bb":
            value = 10
        elif note == "B" or note == "Cb":
            value = 11

        return value


    @classmethod
    def find_neutral_note_with_step(cls, note_letter, step):
        """class method to find target note by giving a step
           (does not consider accidentals)"""

        # translate the letter to ascii code and minus 65 (ascii of "A"), plus a step with modulus of 7
        # since it has 7 neutral notes (C, D, E, F, G, A, B) in music theory
        target_note_number = (ord(note_letter) - 65 + step) % 7

        return chr(target_note_number + 65)

    @classmethod
    def get_interval_note(cls, note, interval_name):
        """get the target interval note by providing a music interval name in Interval class"""

        # get the target interval neutral note without any accidentals
        target_neutral_note_letter = Note.find_neutral_note_with_step(note.base_note, interval_name[0])
        # get the target interval neutral note's pitch number
        target_neutral_note_pitch = Note.letter_to_pitch_number(target_neutral_note_letter)
        # get the exact target note's pitch
        target_pitch = (Note.letter_to_pitch_number(note.base_note) + note.accidental + interval_name[1]) % 12

        interval_difference = target_pitch - target_neutral_note_pitch

        # some special case remedy
        if interval_difference == 11:
            interval_difference = -1
        elif interval_difference == 10:
            interval_difference = -2
        elif interval_difference == -11:
            interval_difference = 1
        elif interval_difference == -10:
            interval_difference = 2

        # create a Note object with info provided
        note = Note(target_pitch, target_neutral_note_letter , interval_difference)

        return note

class Interval:
    """mapping all music interval [neutral step, exact half steps]"""
    perfect_unison = [0, 0]
    minor_second = [1, 1]
    major_second = [1, 2]
    minor_third = [2, 3]
    major_third = [2, 4]
    perfect_fourth = [3, 5]
    augmented_fourth = [3, 6]
    diminished_fifth = [4, 6]
    perfect_fifth = [4, 7]
    minor_sixth = [5, 8]
    major_sixth = [5, 9]
    augmented_sixth = [5, 10]
    diminished_seventh = [6, 9]
    minor_seventh = [6, 10]
    major_seventh = [6, 11]
    perfect_octave = [7, 12]


class Chord:
    """this data structure stores a series of notes"""
    def __init__(self, notes = None):
        """class constructor with two properties
           notes is a list to store all Note objects
           name is a string refers to the name of chord"""
        self.__notes = []
        self.__name = ""

    def chord_major(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.major_third))
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_fifth))
        self.__name = "major chord"

    def chord_minor(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.minor_third))
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_fifth))
        self.__name = "minor chord"

    def chord_major_seventh(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.major_third))
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_fifth))
        self.__notes.append(Note.get_interval_note(note, Interval.major_seventh))
        self.__name = "major 7th chord"

    def chord_minor_seventh(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.minor_third))
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_fifth))
        self.__notes.append(Note.get_interval_note(note, Interval.minor_seventh))
        self.__name = "minor 7th chord"

    def chord_dominant_seventh(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.major_third))
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_fifth))
        self.__notes.append(Note.get_interval_note(note, Interval.minor_seventh))
        self.__name = "dominant 7th chord"

    def chord_german_sixth(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.major_third))
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_fifth))
        self.__notes.append(Note.get_interval_note(note, Interval.augmented_sixth))
        self.__name = "german 6th chord"

    def chord_french_sixth(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.major_third))
        self.__notes.append(Note.get_interval_note(note, Interval.augmented_fourth))
        self.__notes.append(Note.get_interval_note(note, Interval.augmented_sixth))
        self.__name = "french 6th chord"

    def chord_italian_sixth(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.major_third))
        self.__notes.append(Note.get_interval_note(note, Interval.augmented_sixth))
        self.__name = "italian 6th chord"


    def chord_minor_flatted_fifth(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.minor_third))
        self.__notes.append(Note.get_interval_note(note, Interval.diminished_fifth))
        self.__name = "minor flatted fifth"

    def chord_half_diminished_seventh(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.minor_third))
        self.__notes.append(Note.get_interval_note(note, Interval.diminished_fifth))
        self.__notes.append(Note.get_interval_note(note, Interval.minor_seventh))
        self.__name = "half diminished 7th chord"

    def chord_diminished_seventh(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.minor_third))
        self.__notes.append(Note.get_interval_note(note, Interval.diminished_fifth))
        self.__notes.append(Note.get_interval_note(note, Interval.diminished_seventh))
        self.__name = "diminished 7th chord"

    def scale_major(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.major_second))
        self.__notes.append(Note.get_interval_note(note, Interval.major_third))
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_fourth))
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_fifth))
        self.__notes.append(Note.get_interval_note(note, Interval.major_sixth))
        self.__notes.append(Note.get_interval_note(note, Interval.major_seventh))
        self.__name = "major scale"

    def scale_minor_harmonic(self, note):
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_unison))
        self.__notes.append(Note.get_interval_note(note, Interval.major_second))
        self.__notes.append(Note.get_interval_note(note, Interval.minor_third))
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_fourth))
        self.__notes.append(Note.get_interval_note(note, Interval.perfect_fifth))
        self.__notes.append(Note.get_interval_note(note, Interval.minor_sixth))
        self.__notes.append(Note.get_interval_note(note, Interval.major_seventh))
        self.__name = "harmonic minor scale"


    def print_notes(self):
        print("All notes of this chord:")
        for i in self.__notes:
            i.print_note()

    def print_notes_simple(self):
        unison_note_name = self.__notes[0].get_note_name()
        string = ""
        for i in self.__notes:
            string = string + i.get_note_name() + " "
        print("-- " + unison_note_name + " " + self.__name + " -- " + string)

    def print_txt(self, file_name):
        unison_note_name = self.__notes[0].get_note_name()
        string = ""
        for i in self.__notes:
            string = string + i.get_note_name() + " "
        print("\t" + string, file=file_name)

    @classmethod
    def major_roman_number_to_chord(cls, roman_number, note):
        chord = Chord()
        roman = { "I" : chord.chord_major,
                  "bII" : chord.chord_major,
                  "II" : chord.chord_minor,
                  "II7" : chord.chord_minor_seventh,
                  "III" : chord.chord_minor,
                  "IV" : chord.chord_major,
                  "V" : chord.chord_major,
                  "V7" : chord.chord_dominant_seventh,
                  "bVI" : chord.chord_major,
                  "gerVI" : chord.chord_german_sixth,
                  "freVI" : chord.chord_french_sixth,
                  "itaVI" : chord.chord_italian_sixth,
                  "VI" : chord.chord_minor,
                  "VII" : chord.chord_minor_flatted_fifth,
                  "dimVII" : chord.chord_diminished_seventh }
        roman[roman_number](note)
        return chord

    @classmethod
    def minor_roman_number_to_chord(cls, roman_number, note):
        chord = Chord()
        roman = { "I" : chord.chord_minor,
                  "I+" : chord.chord_major,
                  "bII" : chord.chord_major,
                  "II" : chord.chord_minor_flatted_fifth,
                  "II7" : chord.chord_half_diminished_seventh,
                  "III" : chord.chord_major,
                  "IV" : chord.chord_minor,
                  "IV+" : chord.chord_major,
                  "V" : chord.chord_minor,
                  "V+" : chord.chord_major,
                  "V+7" : chord.chord_dominant_seventh,
                  "VI" : chord.chord_major,
                  "gerVI" : chord.chord_german_sixth,
                  "freVI" : chord.chord_french_sixth,
                  "itaVI" : chord.chord_italian_sixth,
                  "VII" : chord.chord_major,
                  "dimVII" : chord.chord_diminished_seventh
                  }
        roman[roman_number](note)
        return chord


if __name__ == "__main__":
    key_name = input("Enter Key Here: ")
    if len(key_name) == 1:
        key_note = Note(Note.letter_to_pitch_number(key_name), key_name[0], 0)
    else:
        if key_name[1] == "b":
            key_note = Note(Note.letter_to_pitch_number(key_name), key_name[0], -1)
        elif key_name[1] == "#":
            key_note = Note(Note.letter_to_pitch_number(key_name), key_name[0], 1)

    chord_list = [ Chord() for i in range(4)]
    chord_list[0].chord_major(key_note)
    chord_list[1].chord_minor(key_note)
    chord_list[2].scale_major(key_note)
    chord_list[3].scale_minor_harmonic(key_note)

    for chord in chord_list:
        chord.print_notes_simple()
