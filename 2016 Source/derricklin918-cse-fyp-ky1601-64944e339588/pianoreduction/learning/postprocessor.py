import os

import music21

from pianoreduction.recognition.eventanalysis.event_analyzer import EventAnalyzer
from pianoreduction.recognition.eventanalysis.chord_flow import FlowState
from pianoreduction.recognition.eventanalysis.lib import MusicManager
from pianoreduction import config
"""
.. module:: postprocessor
    :platform: Unix
    :synopsis: This module's role is to apply additional changes to piano reduction results in MusicXML format.

.. moduleauthor:: Derrick Lin <derricklin918@gmail.com>

Example:
    Run this module standalone to generate a new MusicXML score with additional information
        $ python postprocessor.py
"""

class PostProcessor:
    """
    This class provides methods to embed a MusicXML score with additional information.
    """
    def __init__(self, target ,score, flow = FlowState()):
        """

        :param target: The target score for piano reduction
        :param score: The score after piano reduction
        :param flow: The chord flow object from chord_flow.py
        """
        self._score = score
        self._chord_flow = flow
        self._target = target

        # if target exists, initialize EventAnalyzer for target score
        if target is not None:
            self._event_analyzer = EventAnalyzer(self._target.score, self._chord_flow)
            self._event_analyzer.set_measure_by_score(self._target)
        else:
        # else, initialize EventAnalyzer for
            self._event_analyzer = EventAnalyzer(self._score, self._chord_flow)
        self.analyze()

    @classmethod
    def processor_with_score(cls, score, flow=FlowState()):
        """

        :param score: the music21.score.Score for post processor
        :param flow: the chord flow object from chord_flowpy
        :return: PostProcessor object
        """
        process = cls(None, score, flow)
        return process

    def analyze(self):
        """
        Start chord identification and modulation recognition.
        """
        self._event_analyzer.analyze_oo()
        self._event_analyzer.event_container.lazy_delete_duplicated_chord()
        self._event_analyzer.event_container.display()
        self._modulations = self._event_analyzer.get_all_modulations()

    def embed_chords(self):
        """
        Embed chord names using lyric section in MusicXML
        """
        for event_group in self._event_analyzer.event_container.event_groups:
            # print(event_group.measure)
            for event in event_group.events:
                # print(event.offset, event.output_chord, event.duplicated)
                # self._score.getElementsByClass("Part")[0]..getElementsByOffset(event.offset).getElementsByClass(music21.note.GeneralNote)[0].lyric = event.output_chord
                if not event.duplicated:
                    self._score.measure(event_group.measure).flat.notes.getElementsByOffset(event.offset)[0].lyric = event.chord

    # TODO: Comments and refactor
    def embed_romans(self):
        """
        Embed roman numerals and modulations using lyric section in MusicXML
        """
        #measure starts from 1
        starting_measure = 1
        starting_offset = 0
        for segment in self._modulations:
            # build the roman chord dictionary with key pitch and key quality
            chord_dict = MusicManager.get_instance().make_dict(segment[2], segment[-1])
            key_quality = "" if segment[-1] else "m"
            music_key = self._b_flat_fixer(segment[2]) + key_quality

            # get events between a single modulation
            events_between = self._event_analyzer.event_container.events_between(starting_measure, starting_offset, segment[0], segment[1])
            for i in range(len(events_between)):
                # get roman chord notation from matched chord
                if events_between[i].chord in chord_dict:
                    matched_chord = chord_dict[events_between[i].chord]
                    # print(matched_chord)
                else:
                    matched_chord = ""
                if not events_between[i].duplicated:
                    if i == 0:
                        # for first event of a single modulation, append the key name also.
                        notes = self._score.measure(events_between[i].event_group.measure).flat.notes.getElementsByOffset(events_between[i].offset)
                        if len(notes) != 0:
                            notes[0].lyric = music_key + " " + matched_chord
                    else:
                        notes = self._score.measure(events_between[i].event_group.measure).flat.notes.getElementsByOffset(events_between[i].offset)
                        if len(notes) != 0:
                            notes[0].lyric = matched_chord

            starting_measure = segment[0]
            starting_offset = segment[1]

        # embed chords for all measures left
        events_between = self._event_analyzer.event_container.events_between(starting_measure, starting_offset, self._event_analyzer.number_of_measures, 0)
        for event in events_between:
            if event.chord in chord_dict:
                matched_chord = chord_dict[event.chord]
            else:
                matched_chord = ""
            if not event.duplicated:
                notes = self._score.measure(event.event_group.measure).flat.notes.getElementsByOffset(event.offset)
                if len(notes) != 0:
                    notes[0].lyric = matched_chord

    def color_dissonance(self):
        """
        Color all dissonance in red
        """
        for event_group in self._event_analyzer.event_container.event_groups:
            for event in event_group.events:
                for note_obj in self._score.measure(event.event_group.measure).flat.notes.getElementsByOffset(event.offset):
                        if isinstance(note_obj, music21.chord.Chord):
                            for note in note_obj:
                                if note.name in event.dissonance:
                                    # print(event.event_group.measure, event.global_index, note.name)
                                    note.color = "#ff0000"
                        else:
                            if note_obj.name in event.dissonance:
                                # print(event.event_group.measure, event.global_index, note_obj.name)
                                note_obj.color = "#ff0000"


    def fill_meta_data(self, username, score_name):
        """
        :param username: the name of user
        :param score_name: the name of score
        """
        self._score.metadata = music21.metadata.Metadata()
        self._score.metadata.composer = "Arranged by " + username
        self._score.metadata.title = "Piano reduction: " + score_name

    def _b_flat_fixer(self, str):
        """replace all \"-\" sign with b

        :param str: input str
        Returns:
            str: output with '-' replaced by 'b'
        """
        if str is None:
            return str

        new_str = str.replace("-", "b")

        return new_str

# post process a score
if __name__ == "__main__":
    file_path = os.path.join(config.SCORE_DIR, "test_scores/canon_in_D_excerpt_1.xml")
    s = music21.converter.parse(file_path)
    process = PostProcessor.processor_with_score(s)
    # embed romans
    process.embed_romans()
    # color dissonance
    process.color_dissonance()
    # show the score in notation software
    process._score.show("musicxml")

