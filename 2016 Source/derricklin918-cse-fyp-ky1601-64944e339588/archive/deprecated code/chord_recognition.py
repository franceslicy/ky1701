# ------------------------
# This file has been deprecated but it is kept for reference purpose.
# ------------------------
import os
from collections import Counter

from pianoreduction.recognition.eventanalysis.lib import *
from pianoreduction.recognition.eventanalysis.lib import MusicManager
from pianoreduction import config

# TODO: refactor all to lib.py
def checkEqualIvo(lst):
    return not lst or lst.count(lst[0]) == len(lst)

class MusicScore:
    """This class serves as main entry point for chord recognition"""
    file_path = config.SCORE_DIR

    # the number of sharps/flats to music keys:[major, minor]
    circle_of_fifth_map = {-7: ["Cb"],
                           -6: ["Gb", "Eb"],
                           -5: ["Db", "Bb"],
                           -4: ["Ab", "F"],
                           -3: ["Eb", "C"],
                           -2: ["Bb", "G"],
                           -1: ["F", "D"],
                           0: ["C", "A"],
                           1: ["G", "E"],
                           2: ["D", "B"],
                           3: ["A", "F#"],
                           4: ["E", "C#"],
                           5: ["B", "G#"],
                           6: ["F#", "D#"],
                           7: ["C#"]
                           }

    @property
    def file_name(self):
        """the name of target file"""
        return self._file_name

    @property
    def score(self):
        """store the music21.stream.Score object"""
        return self._score

    @property
    def score_title(self):
        """the title of the score"""
        return self._score_title

    # will be obsolete
    @property
    def chord_table(self):
        """roman number , chord notes tuple"""
        return self._chord_table

    @property
    def full_chord_table(self):
        return self._full_chord_table

    @property
    def measure_chord_info(self):
        """a list contains chords partitioned by measures"""
        return self._measure_chord_info

    @property
    def number_of_measures(self):
        """read-only property: the total number of measures of the score"""
        return self._number_of_measures

    @property
    def measures(self):
        """read-only property: a list of list of notes in measures"""
        return self._measures

    def __init__(self, file_name):
        self._measure_chord_info = []
        self._chord_table = []
        print("initializing chord recognition program...")
        self._file_name = file_name
        self._score = music21.converter.parse(os.path.join(MusicScore.file_path, file_name))
        self._score_title = self._score.metadata.title

        # get first measure of a part to determine the key signature,
        # assuming it remains unchanged through out the score
        measures = self._score.getElementsByClass(music21.stream.Part)[0].getElementsByClass(music21.stream.Measure)
        self._number_of_measures = len(measures)

        # initialize chord table
        self._full_chord_table = MusicManager.make_table_full(MusicManager.all_pitch_class)

        # extract all notes measures by measures from the score
        self._measures = []
        for i in range(1, self.number_of_measures + 1):
            note_stream = self.score.measure(i).flat.notes
            crude_note_list = []
            for note_obj in note_stream:
                if isinstance(note_obj, music21.chord.Chord):
                    for note in note_obj:
                        crude_note_list.append(note)
                else:
                    crude_note_list.append(note_obj)
            self._measures.append(crude_note_list)

        print("initialization completed...")
        print("Score Title: " + self._score_title)

    # old chord recognize function, will become obsolete
    def recognize(self):
        """Start the recognition process"""
        print("Start chord recognition on " + self._score_title)

        # get only a stream of music notes (regardless of different parts)
        for i in range(1, self._number_of_measures + 1):
            print("Measure {}".format(i))

            note_obj_list = self._measures[i - 1]  # because measure starts at 1, not 0
            print(note_obj_list)
            note_list = [(note.name, note.octave) for note in note_obj_list]
            note_name_set = set([note[0] for note in note_list])
            
            print(note_name_set)
            for roman in self._chord_table:
                # subset
                if note_name_set >= set(roman[0]):
                    number = roman[1]
                    # create a note list with all dissonance (not chord tones) removed i.e. only chord tones
                    corr_list = [note for note in note_list if set(note[0]) <= set(roman[0])]
                    print(corr_list)
                    # create a list with only octave number
                    octave_list = [note[1] for note in corr_list]
                    # check if these notes are in the same octave
                    equal = checkEqualIvo(octave_list)
                    # if true, compare their pitch number to find the bass note
                    if equal:
                        max_num = float("inf")
                        bass_note = None
                        for note in corr_list:
                            pitch_number = Interval.letter_to_pitch_number(note[0])
                            if pitch_number < max_num:
                                max_num = pitch_number
                                bass_note = note
                        voicing = "Close Position"

                    else:
                        # find the bass note in the chord with lowest octave
                        bass_note = min(corr_list, key = lambda t: t[1])
                        voicing = "Open Position"
                    # find inversion
                    inversion_number = roman[0].index(bass_note[0])
                    inversions = {0 : "Root Position",
                                  1 : "First Inversion",
                                  2 : "Second Inversion",
                                  3 : "Third Inversion"
                                  }
                    print("{} {} {}".format(number, inversions[inversion_number], voicing))

    # new chord recognize function
    def recognize_new(self):
        """Start the chord recognition process"""
        print("Start chord recognition on " + self._score_title)
        current_table = self._full_chord_table
        # iterate the music score two times
        for i in range(0, 1):
            # print("========= epoch {} ==========".format(i))
            # key_matched list to contain all key that exist in the score
            key_matched = []
            self._measure_chord_info = []
            # get only a stream of music notes (regardless of different parts)
            for i in range(1, self._number_of_measures + 1):
                # print("Measure {}".format(i))
                # get a list of music21.note.Note object in a particular measure
                note_obj_list = self._measures[i - 1]  # because measure starts at 1, not 0
                # convert to a list of tuple(note name, its octave)
                note_list = [(note.name, note.octave) for note in note_obj_list]
                # convert to set (eliminate note with same name
                note_name_set = set([note[0] for note in note_list])

                measure_chord_list = []
                for key, chord_table in current_table[0].items():
                    has_key = False

                    for roman in chord_table:
                        # subset
                        if note_name_set >= set(roman[0]):
                            has_key = True
                            roman_number = roman[1]
                            # create a note list with all dissonance (not chord tones) removed i.e. only chord tones
                            correct_list = [note for note in note_list if {note[0]} <= set(roman[0])]
                            # find the bass note and voicing from correct_list
                            bass_note, voicing = self.__find_voicing_and_bass_note(correct_list)
                            # find inversion with known bass note
                            # 0 = root position 1 = first inversion 2 = second inversion 3 = third inversion
                            inversion_number = roman[0].index(bass_note[0])
                            # print("{} {} {} {}".format(key, roman_number, inversion_number, voicing))
                            single_chord = {"key" : key,
                                            "roman" : roman_number,
                                            "inversion" : inversion_number,
                                            "voicing" : voicing}
                            # append the possible chords of all keys
                            measure_chord_list.append(single_chord)

                    if has_key:
                        key_matched.append(key)
                if len(measure_chord_list) == 0:
                    note_list = list(note_name_set)
                    self._measure_chord_info.append(note_list)
                else:
                    self._measure_chord_info.append(measure_chord_list)

            counts = Counter(key_matched)
            print(counts)

            current_table = MusicManager.make_table_full(name[0] for name in counts.most_common(1))

    def __find_voicing_and_bass_note(self, correct_note_list):
        """Private helper method to find voicing and the bass note of a chord"""
        # create a list with only octave number
        octave_list = [note[1] for note in correct_note_list]
        # check if these notes are in the same octave
        equal = checkEqualIvo(octave_list)
        # if true, compare their pitch number to find the bass note
        if equal:
            max_num = float("inf")
            bass_note = None
            for note in correct_note_list:
                pitch_number = Interval.letter_to_pitch_number(note[0])
                if pitch_number < max_num:
                    max_num = pitch_number
                    bass_note = note
            voicing = "Close Position"

        else:
            # find the bass note in the chord with lowest octave
            bass_note = min(correct_note_list, key=lambda t: t[1])
            voicing = "Open Position"

        return bass_note, voicing

    def print_result(self):
        """print out recognition result"""
        inversions = {0: "Root Position",
                      1: "First Inversion",
                      2: "Second Inversion",
                      3: "Third Inversion"
                      }
        for index, measure in enumerate(self._measure_chord_info):
            print("Measure {}".format(index + 1))
            if isinstance(measure[0], dict):
                for chord in measure:
                    print("{} {} {} {}".format(chord["key"], chord["roman"], inversions[chord["inversion"]], chord["voicing"]))
            else:
                print(measure)


# Unit test main method
if __name__ == "__main__":
    # s = MusicScore("quartet-in-c-major.xml")
    s = MusicScore("SQ-Original-fixed.xml")
    s.recognize_new()
    s.print_result()