from pianoreduction.recognition.eventanalysis.eventtester import EventTester

"""
.. module:: eventstatistics
    :platform: Unix
    :synopsis: This module is created for statistics analysis.

.. moduleauthor:: Derrick Lin <derricklin918@gmail.com>
"""

class EventStatistics:
    """It is the class for statistical analysis. Analysis result can be found in KY1601 final report.
    For actual usage, see pianoreduction/recognition/test.py

    Attributes:
        datasets ([str]): a list of file names pointing to music scores.
        dataset_testers ([recognition.eventanalysis.eventtester.EventTester)]: a list of EventTester objects created from datasets
        total_chord_event (int): the number of total events
        total_recognized_chords (int): the number of events that can be recognized as a legitimate chord
        total_correct_chords_exact (int): the number of exactly correct chords
        total_correct_chords_overly (int): the number of overly recognized chords
        total_correct_chords_different_bass (int): the number of correct chords but with different bass note
        total_correct_chords_same_functionality (int): the number of correct chords that have similar functionality
        total_wrong_chords (int): the number of wrong chords. It is legitimate but totally wrong.
    """
    @property
    def chords_recognized_percentage(self):
        """The percentage of all recognized chords out of total chords"""
        fraction = self._total_recognized_chords / self._total_chord_events * 100
        return round(fraction, 2)

    @property
    def percentage_chords_exact(self):
        """The percentage of all excatly correct chords out of all recognized chords"""
        fraction = self._total_correct_chords_exact / self._total_recognized_chords * 100
        return round(fraction, 2)

    @property
    def percentage_chords_overly(self):
        """The percentage of all overly recognized chords out of all recognized chords"""
        fraction = self._total_correct_chords_overly / self._total_recognized_chords * 100
        return round(fraction, 2)

    @property
    def percentage_chords_different_bass(self):
        """The percentage of all correct chords with different bass note out of all recognized chords"""
        fraction = self._total_correct_chords_different_bass / self._total_recognized_chords * 100
        return round(fraction, 2)

    @property
    def percentage_chords_same_functionality(self):
        """The percentage of all chords with similar functionality out of all recognized chords"""
        fraction = self._total_correct_chords_same_functionality / self._total_recognized_chords * 100
        return round(fraction, 2)

    @property
    def percentage_chords_wrong(self):
        """The percentage of total wrong chords out of recognized chords"""
        fraction = self._total_wrong_chords / self._total_recognized_chords * 100
        return round(fraction, 2)

    def __init__(self, dataset):
        """
        Constructor
        :param dataset: a list of file names
        """
        self._datasets = dataset
        self._dataset_testers = []
        for data in dataset:
            event_tester = EventTester(data)
            event_tester.load_result_file()
            event_tester.start_testing()
            self._dataset_testers.append(event_tester)

        self._total_chord_events = 0
        self._total_recognized_chords = 0
        self._total_correct_chords_exact = 0
        self._total_correct_chords_overly = 0
        self._total_correct_chords_different_bass = 0
        self._total_correct_chords_same_functionality = 0
        self._total_wrong_chords = 0

    def run(self):
        """
        Start testing the dataset
        :return: None
        """
        for dataset in self._dataset_testers:
            self._total_chord_events += dataset._number_of_events
            self._total_recognized_chords += dataset._number_of_recognized_chords

            self._total_correct_chords_exact += dataset.number_of_correct_chords_exact
            self._total_correct_chords_overly += dataset.number_of_correct_chords_overly
            self._total_correct_chords_different_bass += dataset.number_of_correct_chords_wrong_bass
            self._total_correct_chords_same_functionality += dataset.number_of_correct_chords_same_functionality
            self._total_wrong_chords += dataset.number_of_wrong_chords

    def print_result(self):
        """
        Print the testing result to the terminal
        :return: None
        """
        print("Data used for testing:")
        for data in self._datasets:
            print(data)

        print("Total chord events: {}".format(self._total_chord_events))
        print("Total chords recognized: {} ({}%)".format(self._total_recognized_chords, self.chords_recognized_percentage))
        print("Of the recognized chords:")
        print("Total exactly correct chords: {} ({}%)".format(self._total_correct_chords_exact, self.percentage_chords_exact))
        print("Total overly recognized chords: {} ({}%)".format(self._total_correct_chords_overly, self.percentage_chords_overly))
        print("Total same functionality chords: {} ({}%)".format(self._total_correct_chords_same_functionality, self.percentage_chords_same_functionality))
        print("Total wrong bass, same consonance chords: {} ({}%)".format(self._total_correct_chords_different_bass, self.percentage_chords_different_bass))
        print("Total wrong chords: {} {}%".format(self._total_wrong_chords, self.percentage_chords_wrong))