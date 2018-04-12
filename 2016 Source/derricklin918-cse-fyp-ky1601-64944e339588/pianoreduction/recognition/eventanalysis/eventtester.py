# unit testing for event analysis module
import os
import music21
from pianoreduction.recognition.eventanalysis.event_analyzer import EventAnalyzer
from pianoreduction.recognition.eventanalysis.chord_flow import FlowState
from pianoreduction import config

"""
.. module:: eventtester
    :platform: Unix
    :synopsis: This module serves as main class for piano reduction.

.. moduleauthor:: Derrick Lin <derricklin918@gmail.com>

Example:
    Run this module standalone to test a single score, given that the corresponding correct reference data exist
        $ python eventtester.py
"""

class EventTester:
    """This class requires an MusicXML file path input and the reference file for correctness checking

    Attributes:
        file_name (str): the name of MusicXML file
        file_path (str): the file path to the MusicXML file
        result_fp (str): file pointer to reference file
        score (music21.score.Score): music21 score object created from MusicXML file
        event_analyzer (recognition.event_analyzer.EventAnalyzer): being used to recognize chords
        recognized_events ([recognition.eventanalysis.event]): list of events that have a legitimate chord recognized.
        comparison_events ([recognition.eventanalysis.event]): list of events created from reference data for comparision
        wrong_result_events ([recognition.eventanalysis.event]): list of events that are wrongly recognized.
        reasonable_result_events ([recognition.eventanalysis.event]): list of events that are correct in reasonable sense.
    """
    @property
    def soft_correctness_percentage(self):
        """The percentage of soft correctness"""
        return round(self._chord_correctness_soft_fraction * 100, 2)

    @property
    def soft_correctness_overall_percentage(self):
        """The overall percentage of soft correctness"""
        return round(self._overall_correctness_soft_fraction * 100, 2)

    @property
    def medium_correctness_percentage(self):
        """The percentage of medium correctness"""
        return round(self._chord_correctness_medium_fraction * 100, 2)

    @property
    def medium_correctness_overall_percentage(self):
        """The overall percentage of medium correctness"""
        return round(self._overall_correctness_medium_fraction * 100, 2)

    @property
    def hard_correctness_percentage(self):
        """The percentage of hard correctness"""
        return round(self._chord_correctness_hard_fraction * 100, 2)

    @property
    def hard_correctness_overall_percentage(self):
        """The overall percentage of hard correctness"""
        return round(self._overall_correctness_hard_fraction * 100, 2)

    @property
    def acceptable_correctness_percentage(self):
        """The percentage of acceptable correctness"""
        return round(self._chord_correctness_acceptable_fraction * 100, 2)

    @property
    def acceptable_correctness_overall_percentage(self):
        """The overall percentage of acceptable correctness"""
        return round(self._overall_correctness_acceptable_fraction * 100, 2)

    @property
    def recognized_chords_percentage(self):
        """The percentage of recognized chords"""
        return round(self._recognized_chords_fraction * 100, 2)

    @property
    def number_of_correct_chords_exact(self):
        """The number of exactly correct chords"""
        return self._number_of_correct_chords_exact

    @property
    def number_of_correct_chords_overly(self):
        """The number of overly recognized chords"""
        return self._number_of_correct_chords_overly

    @property
    def number_of_correct_chords_wrong_bass(self):
        """The number of correct chords but with different bass"""
        return self._number_of_correct_chords_wrong_bass

    @property
    def number_of_correct_chords_same_functionality(self):
        """The number of chords share similar functionalities"""
        return self._number_of_correct_chords_same_functionality

    @property
    def number_of_wrong_chords(self):
        """The number of wrongly recognized chords"""
        return len(self._wrong_result_events)

    @property
    def percentage_chords_exact(self):
        """The percentage of exactly correct chords"""
        fraction = self._number_of_correct_chords_exact / self._number_of_recognized_chords * 100
        return round(fraction, 2)

    @property
    def percentage_chords_overly(self):
        """The percentage of overly recognized chords"""
        fraction = self._number_of_correct_chords_overly / self._number_of_recognized_chords * 100
        return round(fraction, 2)

    @property
    def percentage_chords_wrong_bass(self):
        """The percentage of correct chords but with different bass"""
        fraction = self._number_of_correct_chords_wrong_bass / self._number_of_recognized_chords * 100
        return round(fraction, 2)

    @property
    def percentage_chords_same_functionality(self):
        """The percentage of correct chords share similar functionalities"""
        fraction = self._number_of_correct_chords_same_functionality / self._number_of_recognized_chords * 100
        return round(fraction, 2)

    @property
    def percentage_chords_wrong(self):
        """The percetage of wrongly recognized chords"""
        fraction = self.number_of_wrong_chords / self._number_of_recognized_chords * 100
        return round(fraction, 2)

    def __init__(self, file_name):
        self._file_name = file_name
        self._file_name_no_ext = os.path.splitext(file_name)[0]
        self._file_path = os.path.join(config.TEST_SCORES_DIR, file_name)
        self._result_fp = None
        self._score = music21.converter.parse(self._file_path)
        self._event_analyzer = EventAnalyzer(self._score, FlowState())
        self._event_analyzer.analyze_oo()
        self._recognized_events = self._event_analyzer.event_container.get_analysis_result()
        self._comparison_events = []
        self._wrong_result_events = []
        self._reasonable_result_events = []
        self._number_of_recognized_chords = 0
        self._number_of_correct_chords_exact = 0
        self._number_of_correct_chords_overly = 0
        self._number_of_correct_chords_wrong_bass = 0
        self._number_of_correct_chords_same_functionality = 0

        # test statistics
        self._recognized_chords_fraction = 0

        self._chord_correctness_soft_fraction = 0
        self._overall_correctness_soft_fraction = 0

        self._chord_correctness_medium_fraction = 0
        self._overall_correctness_medium_fraction = 0

        self._chord_correctness_hard_fraction = 0
        self._overall_correctness_hard_fraction = 0

        self._chord_correctness_acceptable_fraction = 0
        self._overall_correctness_acceptable_fraction = 0

    def load_result_file(self):
        """create file pointer to reference data of same file name and process the data to a list of events for comparison"""
        self._result_fp = open(os.path.join(config.TEST_SCORES_CORRECT_DATA_DIR, self._file_name_no_ext + ".txt"))
        first_line = self._result_fp.readline()
        token = [token.strip() for token in first_line.split(',')]
        self._number_of_events = int(token[1])
        print("File {} Loaded. Total events: {}".format(self._file_name, self._number_of_events))

        for line in self._result_fp:
            token = [token.strip() for token in line.split(',')]
            if len(token) == 4:
                notes = [token[1], token[2], token[3]]
                event = {'index': int(token[0]), 'chord': notes}
                self._comparison_events.append(event)
            elif len(token) == 5:
                notes = [token[1], token[2], token[3], token[4]]
                event = {'index': int(token[0]), 'chord': notes}
                self._comparison_events.append(event)

        # for event in self._recognized_events:
        #     print(event['index'], event['chord'])

    def start_testing(self):
        for i in range(self._number_of_events):
            recognized_chord = self._recognized_events[i]['chord']
            comparison_chord = self._comparison_events[i]['chord']
            event_pitches = self._recognized_events[i]['pitches']
            # if it has matched chords
            if recognized_chord != "n/a":
                self._number_of_recognized_chords = self._number_of_recognized_chords + 1

                p = set(recognized_chord) & set(comparison_chord)
                # print(i,p, set(recognized_chord))
                # equal bass note and same chord notes
                # print(recognized_chord[0], comparison_chord[0])
                # if it has the same chord notes
                if p == set(recognized_chord):
                    # if it has the same bass
                    if recognized_chord[0] == comparison_chord[0]:
                        # print(self._recognized_events[i][0], self._recognized_events[i][1], self._comparison_events[i][1])
                        self._number_of_correct_chords_exact = self._number_of_correct_chords_exact + 1
                    else:
                        self._number_of_correct_chords_wrong_bass = self._number_of_correct_chords_wrong_bass + 1
                        dict = {'index': i, 'recognized': recognized_chord, 'comparison': comparison_chord,
                                'reason': 'wrong bass'}
                        self._reasonable_result_events.append(dict)
                # if overly recognized
                elif len(recognized_chord) - len(p) == 1 and len(recognized_chord) == 4:
                    self._number_of_correct_chords_overly = self._number_of_correct_chords_overly + 1
                    dict = {'index': i, 'recognized': recognized_chord, 'comparison': comparison_chord,
                            'reason': 'overly recognized'}
                    self._reasonable_result_events.append(dict)
                else:
                    recognized_dissonance = set(event_pitches) - set(recognized_chord)
                    comparison_dissonance = set(event_pitches) - set(comparison_chord)
                    # if same dissonance => same chord functionality
                    if recognized_dissonance == comparison_dissonance:
                        self._number_of_correct_chords_same_functionality = self._number_of_correct_chords_same_functionality + 1
                        dict = {'index': i, 'recognized': recognized_chord, 'comparison': comparison_chord,
                                'rec_diss': recognized_dissonance, 'com_diss': comparison_dissonance, 'reason': 'same functionality', "pitches": event_pitches}
                        self._reasonable_result_events.append(dict)
                    else:
                        dict = {'index': i, 'recognized': recognized_chord, 'comparison': comparison_chord,
                                'reason': 'wrong chord'}
                        self._wrong_result_events.append(dict)

        # calcuations of all statistics
        self._recognized_chords_fraction = self._number_of_recognized_chords / self._number_of_events
        self._number_of_soft_correct_chords = self._number_of_correct_chords_exact + self._number_of_correct_chords_wrong_bass + self._number_of_correct_chords_overly + self._number_of_correct_chords_same_functionality
        self._number_of_medium_correct_chords = self._number_of_correct_chords_exact + self._number_of_correct_chords_overly + self._number_of_correct_chords_same_functionality


        self._chord_correctness_soft_fraction = self._number_of_soft_correct_chords / self._number_of_recognized_chords
        self._overall_correctness_soft_fraction = self._number_of_soft_correct_chords / self._number_of_events

        self._chord_correctness_medium_fraction = self._number_of_medium_correct_chords / self._number_of_recognized_chords
        self._overall_correctness_medium_fraction = self._number_of_medium_correct_chords / self._number_of_events

        self._chord_correctness_hard_fraction = self._number_of_correct_chords_exact / self._number_of_recognized_chords
        self._overall_correctness_hard_fraction = self._number_of_correct_chords_exact / self._number_of_events

    def show_test_result(self):
        print("Input: {}, {}".format(self._file_name_no_ext + ".xml", self._file_name_no_ext + ".txt"))
        print("Number of chord events: {}".format(self._number_of_events))
        print("Chords recognized: {} ({}%)\n".format(self._number_of_recognized_chords, self.recognized_chords_percentage))

        print("Exactly correct: {} ({}%)".format(self._number_of_correct_chords_exact, self.percentage_chords_exact))
        print("Overly recognized: {} ({}%)".format(self.number_of_correct_chords_overly, self.percentage_chords_overly))
        print("Similar function: {} ({}%)".format(self.number_of_correct_chords_same_functionality, self.percentage_chords_same_functionality))
        print("Wrong bass, same consonance: {} ({}%)".format(self._number_of_correct_chords_wrong_bass, self.percentage_chords_wrong_bass))
        print("Wrong chords: {} ({}%)\n".format(self.number_of_wrong_chords, self.percentage_chords_wrong))

        print("Correctness analysis:")
        print("Correct chords (hard): {}".format(self._number_of_correct_chords_exact))
        print("Chord correctness (hard): {}%".format(self.hard_correctness_percentage))
        print("Overall correctness (hard): {}%".format(self.hard_correctness_overall_percentage))

        print("Correct chords (normal): {}".format(self._number_of_medium_correct_chords))
        print("Chord correctness (normal): {}%".format(self.medium_correctness_percentage))
        print("Overall correctness (normal): {}%".format(self.medium_correctness_overall_percentage))

        print("Correct chords (soft): {}".format(self._number_of_soft_correct_chords))
        print("Chord correctness (soft): {}%".format(self.soft_correctness_percentage))
        print("Overall correctness (soft): {}%\n".format(self.soft_correctness_overall_percentage))



        for event in self._reasonable_result_events:
            if event['reason'] == "same functionality":
                print("Event {} Recognized: {} Correct: {} Pitches: {} R_diss: {} C_diss {} Reason: {}".format(event['index'], event['recognized'],
                                                                                                               event['comparison'], event['pitches'],
                                                                                                               event['rec_diss'], event['com_diss'],
                                                                                                               event['reason']))
            else:
                print("Event {} Recognized: {} Correct: {} Reason: {}".format(event['index'], event['recognized'],
                                                                          event['comparison'], event['reason']))
        for event in self._wrong_result_events:
            print("Event {} Recognized: {} Correct: {} Reason: {}".format(event['index'], event['recognized'], event['comparison'], event['reason']))

    def write_to_file(self):
        """write to .txt file"""
        with open(os.path.join(config.TEMP_DIR, self._file_name_no_ext + ".txt"), 'w') as f:
            f.write("{}\t{}\n".format(self._file_name_no_ext, self._event_analyzer.event_container.number_of_events))
            for event in self._event_analyzer.event_container.get_analysis_result():
                if len(event[1]) != 0:
                    f.write("{},{}\n".format(event[0], ','.join(event[1])))


if __name__ == "__main__":
    test = EventTester("moonlight_sonata_I_excerpt.xml")
    # test.write_to_file()
    test.load_result_file()
    test.start_testing()
    test.show_test_result()

