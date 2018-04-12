import os

from music21 import *

from pianoreduction import config


class HarmonyDataLoader:
    """class to manage corpus_info.txt"""
    path = os.path.join(config.LIB_DIR, "tonalanalysis")

    def __init__(self, file_name):
        self._fp = open(os.path.join(HarmonyDataLoader.path, "kpcorpus_xml", file_name), 'r')

    # TODO: Refactor
    def process(self):
        # a loop for reading lines
        for line in self._fp:
            # tokenize this line to obtain info of scores
            token = [token.strip() for token in line.split('\t')]
            # init the parser
            # token: 0 : <file.xml> 1 : <score_name> 2: <composer_name> 3 : number of keys occurred
            p = Parser(token[0], token[1], token[2])
            print(token[0], token[1], token[2])
            # a loop to read all keys and chords
            for i in range(int(token[3])):
                line = self._fp.readline()
                # token: 0 : start_of_measure 1 : end_of_measure 2 : tonic 3 : major or minor
                token = [token.strip() for token in line.split('\t')]
                # retrieve the chord marking
                chord_list = p.get_chords_between_offsets(float(token[0]), float(token[1]))
                print(token[0], token[1])
                # pour result to a dictionary
                p.pour_data(chord_list, token[2], token[3])
            # write the result to a new .txt file with same name
            p.write_data()
            # end of loop, ready to parse the next chunk

class Parser:
    """class to parse .xml chord marking data"""
    DIR_NAME = "kpcorpus_xml"
    # path for parsed result

    def __init__(self, file_name, score_name, composer_name):
        # file name without extension
        self._file_name = os.path.splitext(file_name)[0]
        # file name with extension
        self._file_name_with_extension = file_name
        # music21 stream
        self._stream = converter.parse(os.path.join(HarmonyDataLoader.path, "kpcorpus_xml", file_name))
        # name of score
        self._score_name = score_name
        # name of composer
        self._composer_name = composer_name
        # data to be written to txt files
        self._data = []

    def show_stream(self):
        self._stream.show("text")

    def get_chords_between_measures(self, number_start, number_end):
        self._stream = converter.parse(os.path.join(HarmonyDataLoader.path, "kpcorpus_xml", self._file_name_with_extension))
        chords = []
        # get time signature object
        time_signature = self._stream.flat.getElementsByClass(meter.TimeSignature)[0]
        # convert measure to offset unit
        offset_start = (number_start - 1) * time_signature.numerator / (time_signature.denominator / 4)
        offset_end = (number_end) * time_signature.numerator / (time_signature.denominator / 4)
        # get all notes between two offset
        notes = self._stream.flat.notes.getElementsByOffset(offset_start, offsetEnd=offset_end, includeEndBoundary=False)

        for note in notes:
            if note.lyric is not None:
                chords.append((note.offset, note.lyric))
        return chords

    def get_chords_between_offsets(self, offset_start, offset_end, include=False):
        self._stream = converter.parse(os.path.join(HarmonyDataLoader.path, "kpcorpus_xml", self._file_name_with_extension))
        chords = []
        # get all notes between two offset
        notes = self._stream.flat.notes.getElementsByOffset(offset_start, offsetEnd=offset_end, includeEndBoundary=include)

        for note in notes:
            if note.lyric is not None:
                chords.append((note.offset, note.lyric))
        return chords

    def pour_data(self, chord_list, tonic, key_name):
        """pour music key and chord list to a dictionary for later use"""
        key = "{}\t{}".format(tonic, key_name)
        result = []
        result.append(key)
        result.append(chord_list)
        self._data.append(result)

    def write_data(self):
        """write the dictionary to a .txt file for advanced processing"""
        file_name = self._file_name + ".txt"
        file_path = os.path.join(config.DATA_DIR, "corpus_data", file_name)
        with open(file_path, 'w') as f:
            f.write("{}\t{}\t{}\n".format(self._file_name_with_extension, self._score_name, self._composer_name))
            for tuple in self._data:
                f.write("{}\t{}\n".format(tuple[0], len(tuple[1])))
                for chord in tuple[1]:
                    f.write("{}\n".format(chord[1]))

    def print_data(self):
        """print data to the terminal"""
        print("{}\t{}\t{}".format(self._file_name_with_extension, self._score_name, self._composer_name))
        for tuple in self._data:
            print("{}\n".format(tuple[0]))
            for chord in tuple[1]:
                print("{}\t{}\n".format(chord[0], chord[1]))

    # Unit test main method
if __name__ == "__main__":
    h = HarmonyDataLoader("corpus_info.txt")
    h.process()

