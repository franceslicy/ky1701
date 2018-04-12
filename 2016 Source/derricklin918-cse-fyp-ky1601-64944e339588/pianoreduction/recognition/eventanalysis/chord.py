from enum import Enum
from pianoreduction.recognition.eventanalysis.lib import *
"""
.. module:: chord
    :platform: Unix
    :synopsis: This module adds classes useful for storing chord data

.. moduleauthor:: Derrick Lin <derricklin918@gmail.com>

Example:
    Run this module standalone to show how chord class is used.
        $ python chord.py
"""
class Inversion(Enum):
    """
    Mapping all inversions as enumerations.
    """
    undecided = -1
    root_position = 0
    first_inversion = 1
    second_inversion = 2
    third_inversion = 3

class Voicing(Enum):
    """
    Mapping all voicing as enumerations.
    """
    undecided = -1
    close_position = 0
    open_position = 1

class Chord:
    """
    This class store intends to store related information of a chord
    """
    @property
    def chord_pitches(self):
        """all pitches of chord as a list"""
        return self._chord_pitches

    @property
    def bass_note(self):
        """the bass note of this chord"""
        return self._bass_note

    @property
    def inversion(self):
        """Get or set the inversion of this chord"""
        return self._inversion

    @property
    def chord(self):
        """return a chord as a string of pitches with ordered by its inversion"""
        # if the chord is a triad
        if len(self._chord_pitches) == 3:
            if self._inversion == Inversion.root_position:
                return "".join(self._chord_pitches)
            elif self._inversion == Inversion.first_inversion:
                return "".join(inversion_6(self._chord_pitches))
            elif self._inversion == Inversion.second_inversion:
                return "".join(inversion_6_4(self._chord_pitches))
            else:
                return "".join(self._chord_pitches)
        # if the chord is a seventh chord
        elif len(self._chord_pitches) == 4:
            if self._inversion == Inversion.root_position:
                return "".join(self._chord_pitches)
            elif self._inversion == Inversion.first_inversion:
                return "".join(inversion_6_5(self._chord_pitches))
            elif self._inversion == Inversion.second_inversion:
                return "".join(inversion_4_3(self._chord_pitches))
            elif self._inversion == Inversion.third_inversion:
                return "".join(inversion_4_2(self._chord_pitches))
            else:
                return "".join(self._chord_pitches)




    def __init__(self, pitch_list="", bass_note=""):
        """
        Constructor of chord
        :param pitch_list: list of pitches
        :param bass_note: bass note
        """
        self._chord_pitches = pitch_list
        self._bass_note = bass_note
        self._inversion = -1
        for i in range(len(pitch_list)):
            if pitch_list[i] == bass_note:
                if i == 0:
                    self._inversion = Inversion.root_position
                elif i == 1:
                    self._inversion = Inversion.first_inversion
                elif i == 2:
                    self._inversion = Inversion.second_inversion
                elif i == 3:
                    self._inversion = Inversion.third_inversion
                else:
                    self._inversion = Inversion.undecided


    def print_out(self):
        """print all chord information to terminal"""
        print("{} {} {}".format(self._chord_pitches, self._bass_note, self._inversion))

class DetailedChord(Chord):
    """
    This class extends class Chord and add several new properties.
    """
    @property
    def music_key(self):
        """the music key of this chord"""
        return self._music_key

    @property
    def roman_number(self):
        """the roman number of this chord"""
        return self._roman_number

    @property
    def voicing(self):
        """the voicing of this chord"""
        return self._voicing

    @voicing.setter
    def voicing(self, value):
        self._voicing = value


    def __init__(self, pitch_list, bass_note, music_key, roman_number, voicing):
        """Constructor of detailed chord"""
        super().__init__(pitch_list, bass_note)
        self._music_key = music_key
        self._roman_number = roman_number
        self._voicing = voicing

    def print_chord(self):
        """print information of a chord to the terminal"""
        print("{} {} {} {}".format(self._music_key, self._roman_number, self.inversion, self.voicing))

# Unit test main method
if __name__ == "__main__":
    # chord = Chord(music_key="C", roman_number="I", inversion=Inversion.root_position, voicing=Voicing.open_position)
    # chord.print_chord()
    pitches = ["D", "F", "A", "C"]
    chord = Chord(pitches, "C")
    print(chord.chord)