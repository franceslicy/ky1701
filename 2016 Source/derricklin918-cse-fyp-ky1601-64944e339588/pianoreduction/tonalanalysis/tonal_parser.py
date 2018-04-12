import os

import music21

import pianoreduction.tonalanalysis.weka_preprocess as Preprocess
from pianoreduction.recognition.eventanalysis.lib import Interval, MusicManager
from pianoreduction import config


class CorpusManager:
    DATA_FOLDER_DIR = "tonal_result"
    HARMONY_DATA_DIR = "corpus_data"

    def __init__(self):
        self._list_of_files = os.listdir(os.path.join(config.DATA_DIR, CorpusManager.HARMONY_DATA_DIR))

class Tone:
    inversion_dict = {"triad": {0: "",
                                1: "6",
                                2: "64"},
                      "seventh": {0: "7",
                                  1: "65",
                                  2: "43",
                                  3: "42"}
                     }
    triad_list = ["maj", "min", "dim"]
    seventh_list = ["maj7", "min7", "hdim", "fdim", "dom7"]
    special_list = ["Ger6", "Fr6" "It6"]
    special_dict = {"Ger6" : "ger",
                    "ger6" : "ger",
                    "Fr6" : "fre",
                    "fr6" : "fre",
                    "It6" : "ita",
                    "it6" : "ita"}

    major_progression_possible = {"I" : ["maj"],
                                  "bII" : ["maj"],
                                  "II" : ["min"],
                                  "III" : ["min"],
                                  "IV" : ["maj"],
                                  "V" : ["maj, dom7"],
                                  "bVI" : ["maj"],
                                  "VI" : ["min"],
                                  "VII" : ["dim", "dim7"],
                                  }
    minor_progression_possible = {"I" : ["min", "maj"],
                                  "bII" : ["maj"],
                                  "II" : ["dim", "hdim"],
                                  "III" : ["maj"],
                                  "IV" : ["min", "maj"],
                                  "V" : ["min", "maj", "dom7"],
                                  "VI" : ["maj"],
                                  "VII" : ["maj", "dim7"]}



    def __init__(self, root, quality, inversion_number, key_tuple):
        self._tonic = key_tuple[0]
        self._is_major = key_tuple[1]
        self._root = root
        self._quality = quality
        self._inversion_number = inversion_number
        self._roman_dict = self.__build_roman_dict(self._tonic, self._is_major)

    def get_roman_chord_name(self):
        if self._root in self._roman_dict:
            roman_number = self._roman_dict[self._root]
            inversion = ""
            prefix = ""
            suffix = ""
            if roman_number == "VII" and self._quality in ["hdim", "fdim"]:
                prefix = "dim"
            if self._is_major == False:
                if roman_number in ["I", "IV"] and self._quality == "maj":
                    suffix = "+"
                elif roman_number in ["V"] and  (self._quality == "maj" or self._quality == "dom7"):
                    suffix = "+"

            if self._quality in Tone.triad_list:
                if self._inversion_number in Tone.inversion_dict["triad"]:
                    inversion = Tone.inversion_dict["triad"][self._inversion_number]
            elif self._quality in Tone.seventh_list:
                if self._inversion_number in Tone.inversion_dict["seventh"]:
                    inversion = Tone.inversion_dict["seventh"][self._inversion_number]

            # change I64 to Cadential 64 (V64)
            if roman_number == "I" and inversion == "64":
                roman_number = "V"

            roman_chord_name = "{}{}{}{}".format(prefix, roman_number, suffix, inversion)
            return roman_chord_name
        elif self._root == "X":
            prefix = Tone.special_dict[self._quality]
            roman_chord_name = "{}VI".format(prefix)
            return roman_chord_name
        else:
            return

    def __build_roman_dict(self, tonic, is_major):
        roman_dict = {}
        music21_tonic = music21.note.Note(tonic)
        if is_major == True:
            for chord in MusicManager.major_progression_simple:
                roman_dict[Interval.get_interval_note(music21_tonic, chord[1]).name] = chord[0]
        else:
            for chord in MusicManager.minor_progression_simple:
                roman_dict[Interval.get_interval_note(music21_tonic, chord[1]).name] = chord[0]
        return roman_dict


class TonalData:

    def __init__(self, file_name, output_file_name):
        print(file_name)
        self._fp = open(os.path.join(config.DATA_DIR, CorpusManager.HARMONY_DATA_DIR, file_name))
        self._roman_dict = {}
        self._output_file_name = output_file_name
        self._save_major = []
        self._save_minor = []

    def process(self):
        # a loop for reading lines
        line = self._fp.readline()
        meta_data = [token.strip() for token in line.split("\t")]
        for line in self._fp:
            key_data = [token.strip() for token in line.split("\t")]
            tonic = key_data[0].replace("b", "-")
            is_major = True if key_data[1] == "Major" else False
            no_of_chords = int(key_data[2])

            key_tuple = (tonic, is_major)
            chord_data = []
            for i in range(no_of_chords):
                line = self._fp.readline().strip()
                token = line.split("_")
                tone = Tone(token[0].replace("b", "-"), token[1], int(token[2]), key_tuple)

                chord_data.append(tone.get_roman_chord_name())

            if is_major == True and len(chord_data) > 0:
                self._save_major.append(chord_data)
            elif is_major == False and len(chord_data) > 0:
                self._save_minor.append(chord_data)

            self.write_to_file_with_data_list(chord_data)

    def write_to_file_with_data_list(self, data_list):
        file_path = os.path.join(config.DATA_DIR, CorpusManager.DATA_FOLDER_DIR, self._output_file_name)
        # TODO: handle the creation of directory and the output .txt file if not exists
        with open(file_path, 'a') as f:
            for data in data_list:
                f.write("{}\n".format(data))
            f.write("----------------------\n")

# Unit test main method
if __name__ == "__main__":
    c = CorpusManager()
    major_save = []
    minor_save = []
    for file in c._list_of_files:
        t = TonalData(file, "result.txt")
        t.process()
        major_save = major_save + t._save_major
        minor_save = minor_save + t._save_minor


    # TODO: refactor and modularization
    major_output = []
    for list in major_save:
        target = []
        for chord in list:
            if chord in MusicManager.major_progression_extend_index:
                target.append(chord)
            else:
                target.append("N/A")
        print(target)
        if target != []:
            major_output = major_output + Preprocess.ext_other_key(Preprocess.n_trans(target,2), True)
            print(major_output)

    major_output = [row for row in major_output if "N/A" not in row]

    minor_output = []
    for list in minor_save:
        target = []
        for chord in list:
            if chord in MusicManager.minor_progression_extend_index:
                target.append(chord)
            else:
                target.append("N/A")
        print(target)
        if target != []:
            minor_output = minor_output + Preprocess.ext_other_key(Preprocess.n_trans(target, 2), False)
            print(minor_output)

    minor_output = [row for row in minor_output if "N/A" not in row]

    major_result = [["1","2","Trans","Match","Major"]]+[x for x in major_output if x[-1] == "Major"] + [x for x in minor_output if x[-1] == "Major"]
    minor_result = [["1","2","Trans","Match","Major"]]+[x for x in major_output if x[-1] == "Minor"] + [x for x in minor_output if x[-1] == "Minor"]
    print("Major: ",major_result)
    print("Minor: ",minor_result)
    Preprocess.save_list('weka_major.csv', major_result)
    Preprocess.save_list('weka_minor.csv', minor_result)