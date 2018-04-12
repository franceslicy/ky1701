# CUHK CSE FYP 2016 Piano Reduction Task 1
# LIN Hang Yu AU Ho Wing
# Superviser: Prof. Kevin Yip
# Co-superviser: Prof. Lucas Wong
import music21
from itertools import permutations

# all inversion rules to reorder the chord structure
# for triads
def appender_3(chord, first, second, third):
    new_chord = []
    new_chord.append(chord[first])
    new_chord.append(chord[second])
    new_chord.append(chord[third])
    return new_chord

def appender_4(chord, first, second, third, fourth):
    new_chord = []
    new_chord.append(chord[first])
    new_chord.append(chord[second])
    new_chord.append(chord[third])
    new_chord.append(chord[fourth])
    return new_chord

def inversion_6(chord):
    return appender_3(chord, 1, 2, 0)

def inversion_6_4(chord):
    return appender_3(chord, 2, 0, 1)

# for seventh chords
def inversion_6_5(chord):
    return appender_4(chord, 1, 2, 3, 0)

def inversion_4_3(chord):
    return appender_4(chord, 2, 3, 0, 1)

def inversion_4_2(chord):
    return appender_4(chord, 3, 0, 1, 2)

class Interval:
    """
    This class provides class methods to handle music intervals and build chords from chord progression
    """

    # intervals to [step different, pitch different]
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

    # chords to corresponding intervals
    chord_major = [perfect_unison, major_third, perfect_fifth]
    chord_minor = [perfect_unison, minor_third, perfect_fifth]
    chord_major_seventh = [perfect_unison, major_third, perfect_fifth, major_seventh]
    chord_minor_seventh = [perfect_unison, minor_third, perfect_fifth, minor_seventh]
    chord_dominant_seventh = [perfect_unison, major_third, perfect_fifth, minor_seventh]
    chord_german_sixth = [perfect_unison, major_third, perfect_fifth, augmented_sixth]
    chord_french_sixth = [perfect_unison, major_third, augmented_fourth, augmented_sixth]
    chord_italian_sixth = [perfect_unison, major_third, augmented_sixth]
    chord_minor_flatted_fifth = [perfect_unison, minor_third, diminished_fifth]
    chord_half_diminished_seventh = [perfect_unison, minor_third, diminished_fifth, minor_seventh]
    chord_diminished_seventh = [perfect_unison, minor_third, diminished_fifth, diminished_seventh]

    @classmethod
    def get_interval_note(cls, note, interval_name):
        """
        get the target interval note (with music21.note.Note type) by providing a music interval name
        in Interval class
        """

        # get the target interval neutral note without any accidentals
        target_neutral_note_letter = Interval.find_neutral_note_with_step(note, interval_name[0])
        # get the target interval neutral note's pitch number
        target_neutral_note_pitch = Interval.letter_to_pitch_number(target_neutral_note_letter)
        # get the exact target note's pitch
        target_pitch = (note.pitch.pitchClass + interval_name[1]) % 12

        interval_difference = target_pitch - target_neutral_note_pitch
        # print(interval_difference)

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
        note = music21.note.Note(target_neutral_note_letter)
        note.pitch.accidental = interval_difference

        return note

    @classmethod
    def find_neutral_note_with_step(cls, note, step):
        """
        class method to find target note by giving a step
           (omit accidentals)
           """

        # translate the letter to ascii code and minus 65 (ascii of "A"), plus a step with modulus of 7
        # since it has 7 neutral notes (C, D, E, F, G, A, B) in music theory
        target_note_step_number = (ord(note.step) - 65 + step) % 7

        return chr(target_note_step_number + 65)

    @staticmethod
    def letter_to_pitch_number(pitch_class):
        corrected_pitch_class = pitch_class.replace("-", "b")

        pitch_dict = {'Cbb' : 10,
                      'Cb' : 11,
                      'C' : 0,
                      'C#' : 1,
                      'C##' : 2,
                      'Dbb' : 0,
                      'Db' : 1,
                      "D" : 2,
                      'D#' : 3,
                      'D##' : 4,
                      'Ebb' : 2,
                      'Eb' : 3,
                      'E' : 4,
                      'E#' : 5,
                      'E##' : 6,
                      'Fbb' : 3,
                      'Fb' : 4,
                      'F' : 5,
                      'F#' : 6,
                      'F##' : 7,
                      'Gbb' : 5,
                      'Gb' : 6,
                      'G' : 7,
                      'G#' : 8,
                      'G##' : 9,
                      'Abb' : 7,
                      'Ab' : 8,
                      'A' : 9,
                      'A#' : 10,
                      'A##' : 11,
                      'Bbb' : 9,
                      'Bb' : 10,
                      'B' : 11,
                      'B#' : 0,
                      'B##' : 1}
        if corrected_pitch_class in pitch_dict:
            return pitch_dict[corrected_pitch_class]
        else:
            return -1
    # TODO: relocate this method under MusicManager
    @classmethod
    def major_roman_number_to_chord(cls, note, roman_number, output_name=False):
        """return a chord as a list of notes with type music21.note.Note following major progression"""
        roman = {"I" : Interval.chord_major,
                 "I6" : inversion_6(Interval.chord_major),
                 "I64": inversion_6_4(Interval.chord_major),
                 "bII": Interval.chord_major,
                 "bII6": inversion_6(Interval.chord_major),
                 "II": Interval.chord_minor,
                 "II6": inversion_6(Interval.chord_minor),
                 "II7": Interval.chord_minor_seventh,
                 "II65": inversion_6_5(Interval.chord_minor_seventh),
                 "III": Interval.chord_minor,
                 "III6": inversion_6(Interval.chord_minor),
                 "IV": Interval.chord_major,
                 "IV6": inversion_6(Interval.chord_major),
                 "IV64": inversion_6_4(Interval.chord_major),
                 "V": Interval.chord_major,
                 "V6": inversion_6(Interval.chord_major),
                 "V64": inversion_6_4(Interval.chord_major),
                 "V7": Interval.chord_dominant_seventh,
                 "V65": inversion_6_5(Interval.chord_dominant_seventh),
                 "V43": inversion_4_3(Interval.chord_dominant_seventh),
                 "V42": inversion_4_2(Interval.chord_dominant_seventh),
                 "bVI": Interval.chord_major,
                 "bVI6": inversion_6(Interval.chord_major),
                 "gerVI": Interval.chord_german_sixth,
                 "freVI": Interval.chord_french_sixth,
                 "itaVI": Interval.chord_italian_sixth,
                 "VI": Interval.chord_minor,
                 "VI6": inversion_6(Interval.chord_minor),
                 "VII": Interval.chord_minor_flatted_fifth,
                 "VII6": inversion_6(Interval.chord_minor_flatted_fifth),
                 "dimVII7": Interval.chord_diminished_seventh,
                 "dimVII65": inversion_6_5(Interval.chord_diminished_seventh),
                 "dimVII43": inversion_4_3(Interval.chord_diminished_seventh),
                 "dimVII42": inversion_4_2(Interval.chord_diminished_seventh)
                 }
        note_list = cls.chord(note, roman[roman_number], output_name)
        return note_list

    # TODO: relocate this method under MusicManager
    @classmethod
    def minor_roman_number_to_chord(cls, note, roman_number, output_name=False):
        """return a chord as a list of notes with type music21.note.Note following minor progression"""
        roman = {"I": Interval.chord_minor,
                 "I+": Interval.chord_major,
                 "I6": inversion_6(Interval.chord_minor),
                 "I+6": inversion_6(Interval.chord_major),
                 "I64": inversion_6_4(Interval.chord_minor),
                 "I+64": inversion_6_4(Interval.chord_major),
                 "bII": Interval.chord_major,
                 "bII6": inversion_6(Interval.chord_major),
                 "II": Interval.chord_minor_flatted_fifth,
                 "II6": inversion_6(Interval.chord_minor_flatted_fifth),
                 "II7": Interval.chord_half_diminished_seventh,
                 "II65": inversion_6_5(Interval.chord_half_diminished_seventh),
                 "III": Interval.chord_major,
                 "III6": inversion_6(Interval.chord_major),
                 "IV": Interval.chord_minor,
                 "IV+": Interval.chord_major,
                 "IV6": inversion_6(Interval.chord_minor),
                 "IV+6": inversion_6(Interval.chord_major),
                 "IV64": inversion_6_4(Interval.chord_minor),
                 "IV+64": inversion_6_4(Interval.chord_major),
                 "V": Interval.chord_minor,
                 "V6": inversion_6(Interval.chord_minor),
                 "V64": inversion_6_4(Interval.chord_minor),
                 "V+": Interval.chord_major,
                 "V+6": inversion_6(Interval.chord_major),
                 "V+64": inversion_6_4(Interval.chord_major),
                 "V+7": Interval.chord_dominant_seventh,
                 "V+65": inversion_6_5(Interval.chord_dominant_seventh),
                 "V+43": inversion_4_3(Interval.chord_dominant_seventh),
                 "V+42": inversion_4_2(Interval.chord_dominant_seventh),
                 "VI": Interval.chord_major,
                 "VI6": inversion_6(Interval.chord_major),
                 "gerVI": Interval.chord_german_sixth,
                 "freVI": Interval.chord_french_sixth,
                 "itaVI": Interval.chord_italian_sixth,
                 "VII": Interval.chord_major,
                 "VII6": inversion_6(Interval.chord_major),
                 "dimVII7": Interval.chord_diminished_seventh,
                 "dimVII65": inversion_6_5(Interval.chord_diminished_seventh),
                 "dimVII43": inversion_4_3(Interval.chord_diminished_seventh),
                 "dimVII42": inversion_4_2(Interval.chord_diminished_seventh)
                 }
        note_list = cls.chord(note, roman[roman_number], output_name)
        return note_list

    @classmethod
    def chord(cls, note, chord_name, output_name=False):
        # helper method to build chords
        note_list = []
        if output_name:
            for name in chord_name:
                note_list.append(Interval.get_interval_note(note, name).name)
        else:
            for name in chord_name:
                note_list.append(Interval.get_interval_note(note, name))
        return note_list


class MusicManager(object):
    major_progression = [["I", Interval.perfect_unison],
                         ["bII", Interval.minor_second],
                         ["II", Interval.major_second],
                         ["II7", Interval.major_second],
                         ["III", Interval.major_third],
                         ["IV", Interval.perfect_fourth],
                         ["V", Interval.perfect_fifth],
                         ["V7", Interval.perfect_fifth],
                         ["bVI", Interval.minor_sixth],
                         ["gerVI", Interval.minor_sixth],
                         ["freVI", Interval.minor_sixth],
                         ["itaVI", Interval.minor_sixth],
                         ["VI", Interval.major_sixth],
                         ["VII", Interval.major_seventh],
                         ["dimVII7", Interval.major_seventh]]

    major_progression_extend = [["I", Interval.perfect_unison],
                                ["I6", Interval.perfect_unison],
                                ["I64", Interval.perfect_unison],
                                ["bII", Interval.minor_second],
                                ["bII6", Interval.minor_second],
                                ["II", Interval.major_second],
                                ["II6", Interval.major_second],
                                ["II7", Interval.major_second],
                                ["II65", Interval.major_second],
                                ["III", Interval.major_third],
                                ["III6", Interval.major_third],
                                ["IV", Interval.perfect_fourth],
                                ["IV6", Interval.perfect_fourth],
                                ["IV64", Interval.perfect_fourth],
                                ["V", Interval.perfect_fifth],
                                ["V6", Interval.perfect_fifth],
                                ["V64", Interval.perfect_fifth],
                                ["V7", Interval.perfect_fifth],
                                ["V65", Interval.perfect_fifth],
                                ["V43", Interval.perfect_fifth],
                                ["V42", Interval.perfect_fifth],
                                ["bVI", Interval.minor_sixth],
                                ["bVI6", Interval.minor_sixth],
                                ["gerVI", Interval.minor_sixth],
                                ["freVI", Interval.minor_sixth],
                                ["itaVI", Interval.minor_sixth],
                                ["VI", Interval.major_sixth],
                                ["VI6", Interval.major_sixth],
                                ["VII", Interval.major_seventh],
                                ["VII6", Interval.major_seventh],
                                ["dimVII7", Interval.major_seventh],
                                ["dimVII65", Interval.major_seventh],
                                ["dimVII43", Interval.major_seventh],
                                ["dimVII42", Interval.major_seventh]]

    major_progression_simple = [["I", Interval.perfect_unison],
                                ["bII", Interval.minor_second],
                                ["II", Interval.major_second],
                                ["III", Interval.major_third],
                                ["IV", Interval.perfect_fourth],
                                ["V", Interval.perfect_fifth],
                                ["bVI", Interval.minor_sixth],
                                ["VI", Interval.major_sixth],
                                ["VII", Interval.major_seventh]]

    major_progression_extend_index = [list[0] for list in major_progression_extend]

    minor_progression = [["I", Interval.perfect_unison],
                         ["I+", Interval.perfect_unison],
                         ["bII", Interval.minor_second],
                         ["II", Interval.major_second],
                         ["II7", Interval.major_second],
                         ["III", Interval.minor_third],
                         ["IV", Interval.perfect_fourth],
                         ["IV+", Interval.perfect_fourth],
                         ["V", Interval.perfect_fifth],
                         ["V+", Interval.perfect_fifth],
                         ["V+7", Interval.perfect_fifth],
                         ["VI", Interval.minor_sixth],
                         ["gerVI", Interval.minor_sixth],
                         ["freVI", Interval.minor_sixth],
                         ["itaVI", Interval.minor_sixth],
                         ["VII", Interval.minor_seventh],
                         ["dimVII7", Interval.major_seventh]]

    minor_progression_simple = [["I", Interval.perfect_unison],
                                 ["bII", Interval.minor_second],
                                 ["II", Interval.major_second],
                                 ["III", Interval.minor_third],
                                 ["IV", Interval.perfect_fourth],
                                 ["V", Interval.perfect_fifth],
                                 ["VI", Interval.minor_sixth],
                                 ["VII", Interval.minor_seventh],]

    minor_progression_extend = [["I", Interval.perfect_unison],
                                ["I+", Interval.perfect_unison],
                                ["I6", Interval.perfect_unison],
                                ["I+6", Interval.perfect_unison],
                                ["I64", Interval.perfect_unison],
                                ["I+64", Interval.perfect_unison],
                                ["bII", Interval.minor_second],
                                ["bII6", Interval.minor_second],
                                ["II", Interval.major_second],
                                ["II6", Interval.major_second],
                                ["II7", Interval.major_second],
                                ["II65", Interval.major_second],
                                ["III", Interval.minor_third],
                                ["III6", Interval.minor_third],
                                ["IV", Interval.perfect_fourth],
                                ["IV+", Interval.perfect_fourth],
                                ["IV6", Interval.perfect_fourth],
                                ["IV+6", Interval.perfect_fourth],
                                ["IV64", Interval.perfect_fourth],
                                ["IV+64", Interval.perfect_fourth],
                                ["V", Interval.perfect_fifth],
                                ["V6", Interval.perfect_fifth],
                                ["V64", Interval.perfect_fifth],
                                ["V+", Interval.perfect_fifth],
                                ["V+6", Interval.perfect_fifth],
                                ["V+64", Interval.perfect_fifth],
                                ["V+7", Interval.perfect_fifth],
                                ["V+65", Interval.perfect_fifth],
                                ["V+43", Interval.perfect_fifth],
                                ["V+42", Interval.perfect_fifth],
                                ["VI", Interval.minor_sixth],
                                ["VI6", Interval.minor_sixth],
                                ["gerVI", Interval.minor_sixth],
                                ["freVI", Interval.minor_sixth],
                                ["itaVI", Interval.minor_sixth],
                                ["VII", Interval.minor_seventh],
                                ["VII6", Interval.minor_seventh],
                                ["dimVII7", Interval.major_seventh],
                                ["dimVII65", Interval.major_seventh],
                                ["dimVII43", Interval.major_seventh],
                                ["dimVII42", Interval.major_seventh]]

    minor_progression_extend_index = [list[0] for list in minor_progression_extend]


    all_pitch_class = ["C", "C#", "D-", "D", "D#", "E-", "E", "E#", "F-", "F", "F#", "G-", "G", "G#", "A-", "A", "A#",
                       "B-", "B", "B#", "C-"]

    INSTANCE = None

    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists!")
        self._x = 100

    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = MusicManager()
        return cls.INSTANCE

    def make_table(self, key_name, major=True):
        # make roman number, chord notes table by giving a key.

        # create a music21.note.Note object by a key name e.g. C, D, Eb..
        key_note = music21.note.Note(key_name)

        chord_list = []
        if major:
            for roman_number in MusicManager.major_progression_extend:
                # get the root note corresponding to the roman number.
                tone_note = Interval.get_interval_note(key_note, roman_number[1])
                # append chord of the root note to chord_list
                chord_list.append([Interval.major_roman_number_to_chord(tone_note, roman_number[0], True),
                                   roman_number[0]])
        else:
            for roman_number in MusicManager.minor_progression_extend:
                tone_note = Interval.get_interval_note(key_note, roman_number[1])
                chord_list.append([Interval.minor_roman_number_to_chord(tone_note, roman_number[0], True),
                                   roman_number[0]])

        return chord_list

    def make_dict(self, key_name, major=True):
        # make roman number, chord notes dictionary by giving a key.

        # create a music21.note.Note object by a key name e.g. C, D, Eb..
        key_note = music21.note.Note(key_name)

        chord_dict = {}
        if major:
            for roman_number in MusicManager.major_progression_extend:
                # get the root note corresponding to the roman number.
                tone_note = Interval.get_interval_note(key_note, roman_number[1])
                # append chord of the root note to chord_list
                chord = Interval.major_roman_number_to_chord(tone_note, roman_number[0], True)
                for index in permutations(chord[1:]):
                    chord_dict[chord[0]+","+",".join(index)] = roman_number[0]
        else:
            for roman_number in MusicManager.minor_progression_extend:
                tone_note = Interval.get_interval_note(key_note, roman_number[1])
                chord = Interval.minor_roman_number_to_chord(tone_note, roman_number[0], True)
                for index in permutations(chord[1:]):
                    chord_dict[chord[0]+","+",".join(index)] = roman_number[0]

        return chord_dict

    def make_table_full(self):
        # make roman number, chord notes table by giving a key.
        full_chord_list = []
        major_chord_list = {}
        minor_chord_list = {}
        for key in MusicManager.all_pitch_class:
            key_note = music21.note.Note(key)

            chord_list = []
            for roman_number in MusicManager.major_progression:
                # get the root note corresponding to the roman number.
                tone_note = Interval.get_interval_note(key_note, roman_number[1])
                # append chord of the root note to chord_list
                chord_list.append([Interval.major_roman_number_to_chord(tone_note, roman_number[0], True),
                                   roman_number[0]])
            major_chord_list[key] = chord_list

            chord_list_2 = []
            for roman_number in MusicManager.minor_progression:
                tone_note = Interval.get_interval_note(key_note, roman_number[1])
                chord_list_2.append([Interval.minor_roman_number_to_chord(tone_note, roman_number[0], True),
                                     roman_number[0]])
            minor_chord_list[key] = chord_list_2

        full_chord_list.append(major_chord_list)
        full_chord_list.append(minor_chord_list)
        return full_chord_list

    def make_table_full_extend(self):
        # make roman number, chord notes table by giving a key.
        full_chord_list = []
        major_chord_list = {}
        minor_chord_list = {}
        for key in MusicManager.all_pitch_class:
            key_note = music21.note.Note(key)

            chord_list = []
            for roman_number in MusicManager.major_progression_extend:
                # get the root note corresponding to the roman number.
                tone_note = Interval.get_interval_note(key_note, roman_number[1])
                # append chord of the root note to chord_list
                chord_list.append([Interval.major_roman_number_to_chord(tone_note, roman_number[0], True),
                                   roman_number[0]])
            major_chord_list[key] = chord_list

            chord_list_2 = []
            for roman_number in MusicManager.minor_progression_extend:
                tone_note = Interval.get_interval_note(key_note, roman_number[1])
                chord_list_2.append([Interval.minor_roman_number_to_chord(tone_note, roman_number[0], True),
                                     roman_number[0]])
            minor_chord_list[key] = chord_list_2

        full_chord_list.append(major_chord_list)
        full_chord_list.append(minor_chord_list)
        return full_chord_list

    def make_chord_database(self):
        basic_chords = [Interval.chord_major, Interval.chord_minor,
                        Interval.chord_minor_seventh, Interval.chord_dominant_seventh,
                        Interval.chord_minor_flatted_fifth, Interval.chord_half_diminished_seventh,
                        Interval.chord_diminished_seventh]
        result_list = []
        for key in MusicManager.all_pitch_class:
            key_note = music21.note.Note(key)
            for chord in basic_chords:
                result_list.append(Interval.chord(key_note, chord, True))
        return result_list

if __name__ == "__main__":
    table = MusicManager.get_instance().make_table_full_extend()
    print(table[1]['C'])