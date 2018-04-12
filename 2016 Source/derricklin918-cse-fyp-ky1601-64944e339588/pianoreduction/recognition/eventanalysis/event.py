# ===================
# module: event.py
# description: TODO
# ===================
import logging
import os

from pianoreduction.recognition.eventanalysis.lib import MusicManager, Interval
from pianoreduction import config

# ===== logger setting =====
log_file_name = "event_analyzer_2.log"
log_file_path = os.path.join(config.LOG_DIR, log_file_name)
logger = logging.getLogger("Analyzer")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(name)s %(levelname)s %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

file = logging.FileHandler(log_file_path, mode = 'w')
file.setLevel(logging.DEBUG)

logger.addHandler(file)
# ===== logger setting end =

def remove_identical(list):
    """remove any duplicated elements within a list"""
    seen = set()
    seen_add = seen.add
    return [x for x in list if not (x in seen or seen_add(x))]

class Event:
    @property
    def event_group(self):
        """obj(EventGroup): Store reference to its parent Event Group"""
        return self._event_group

    @property
    def event_container(self):
        """obj(EventContainer): Store reference to the super container"""
        return self._event_container

    @property
    def offset(self):
        """float: Store the beat offset of event"""
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    @property
    def event_index(self):
        return self._event_index

    @property
    def global_index(self):
        return self._global_index

    @property
    def dissonance(self):
        """str: Store the pitch of dissonance found"""
        return self._dissonance

    @property
    def pitch_classes(self):
        """list(str): Store the pitch classes and its octave contained by event"""
        return self._pitch_classes

    @property
    def pitch_classes_octave(self):
        return self._pitch_classes_octave

    @pitch_classes.setter
    def pitch_classes(self, list):
        self._pitch_classes = list

    @property
    def corrected_pitch_classes(self):
        """list(str): the corrected pitch classes of event"""
        return self._corrected_pitch_classes

    @corrected_pitch_classes.setter
    def corrected_pitch_classes(self, list):
        self._corrected_pitch_classes = list

    @property
    def is_chord_match(self):
        """bool: does event match a chord"""
        return self._is_chord_match

    @property
    def matched_chord(self):
        """list(str): the pitch classes of matched chord"""
        return self._matched_chord

    @property
    def chord(self):
        """Chord(obj): the chord object"""
        if len(self._matched_chord) > 0:
            return ",".join(self._matched_chord[0])
        else:
            return ""

    @property
    def bass_note(self):
        """str: the pitch class of bass note"""
        return self._bass_note

    @property
    def bass_tuple(self):
        return self._bass_tuple

    @property
    def duplicated(self):
        return self._duplicated

    @duplicated.setter
    def duplicated(self, boolean):
        self._duplicated = boolean

    def __init__(self, pitch_classes, bass_tuple, offset, event_index, global_index, event_group, event_container):
        self._pitch_classes_octave = pitch_classes
        self._pitch_classes = remove_identical(event_group.sort_single_event_notes(pitch_classes))
        self._corrected_pitch_classes = []
        self._offset = offset
        self._event_index = event_index
        self._global_index = global_index
        self._event_group = event_group
        self._event_container = event_container
        self._bass_tuple = bass_tuple
        self._bass_note = bass_tuple[0]
        self._is_chord_match = False
        self._matched_chord = []
        self._dissonance = ""
        self._key = ""
        self._duplicated = False

    def resolve_base_chord(self, matched_chord):
            result = []
            for pitch in self._corrected_pitch_classes:
                if pitch in matched_chord:
                    # add pitch in corrected pitch class sorted
                    result.append(pitch)
            for pitch in matched_chord:
                if pitch not in self._corrected_pitch_classes:
                    # add pitch not in corrected pitch class
                    result.append(pitch)
            return result

    def match_triad_chord(self, Flow):
        """
        Match pitch class and corrected pitch classes against chord data list
        Args:
            FlowState
        Return:
            None
        """
        self.match_exact_chord(Flow, self._corrected_pitch_classes)
        self.match_exact_chord(Flow, self._pitch_classes)
        return

    def match_exact_chord(self, Flow, chord):
        """
        Match chord against chord data list
        Args:
            FlowState, chord list
        Return:
            None
        """
        if Flow.match_chord_exact(chord):

            self._event_group.add_candidate_chord(chord, self.event_index)
            if len(chord) == 4:
                # Also add the chord without 7
                for chord in Flow.remove_seven_chord(chord):
                    self._event_group.add_candidate_chord(chord, self.event_index)
                    self.add_matched_chord(chord)
                return
            self.add_matched_chord(chord)


    def add_matched_chord(self, matched_chord):
        # Resolve Base of the chord
        self.resolve_base_chord(matched_chord)
        for chord in self._matched_chord:
            if set(chord) == set(matched_chord):
            # Skip if chord already in match
                return
        # Add Chord
        self._matched_chord.append(matched_chord)
        self._event_group.add_candidate_chord(matched_chord, self.event_index)
        return

    def match_candidates(self):
        # for each chord candidate, try matching triads with at least two and three pitches are the same
        candidate_list = []
        for candidate in self._event_group.candidate_chords:
            p = set(candidate[0]) & set(self._corrected_pitch_classes)
            if len(candidate[0]) - len(p) <= 1 and len(candidate[0]) != 4:
                self._is_chord_match = True
                candidate_list.append(self.resolve_base_chord(candidate[0]))
        if self._is_chord_match is True:
            self._matched_chord = candidate_list

    def match_partial(self, Flow):
        if self._is_chord_match is False:
            if len(self._pitch_classes) != 1:
                chord_partials = Flow.match_chord_partial(self._corrected_pitch_classes)
                chord_partials_triad = [chord for chord in chord_partials if len(chord) == 3]
                self._matched_chord += chord_partials_triad
                for chord in chord_partials_triad:
                    self._event_group.add_candidate_chord(chord , self.event_index)
            # if len(self._matched_chord) != 0:
            #     self.match_using_flow(Flow)


    def find_previous_chord(self, chord=[], start=1):
    # This function find chord from start which not much with chord (to find previous n chord)
        i = start
        while i <= self._global_index:
            matched_chord = self._event_container.events[self._global_index - i].matched_chord
            if matched_chord != []:
                if set(self._event_container.events[self._global_index - i].matched_chord[0]) != set(chord):
                    return i
            i = i + 1

        return -1

    def find_next_chord(self, chord=[]):
        i = self._global_index
        while i < len(self._event_container.events):
            matched_chord = self._event_container.events[i].matched_chord
            if matched_chord != []:
                if set(self._event_container.events[i].matched_chord[0]) != set(chord):
                    return i
            i = i + 1
        return -1

    def select_chord(self, all_modulations):
        previous_modulation = []
        for modulation in all_modulations:
            if modulation[0] < self._event_group.measure:
                previous_modulation = modulation
            elif modulation[0] == self._event_group.measure and modulation[1] <= self._offset:
                previous_modulation = modulation

        if previous_modulation == []:
            previous_modulation = all_modulations[0]

        # Set the key of current modulation
        self._key = previous_modulation[2]

        # Find previous_event_chord
        if self._global_index != 0:
            previous_event_chord = self._event_container.events[self._global_index-1].matched_chord[0]
        else:
            previous_event_chord = []

        print(self.event_group.measure, self.global_index, previous_modulation)

        # Set chord according dissonance
        matching_chords = [previous_modulation[4], previous_modulation[3]]

        if previous_modulation[0] == self.event_group.measure and previous_modulation[1] == self.offset:
            index = all_modulations.index(previous_modulation)
            if index > 0:
                previous_modulation = all_modulations[index-1]
                matching_chords = [previous_modulation[4], previous_modulation[3]] + matching_chords

        matching_chords_checked = []
        for chord in self._matched_chord:
            for matching_chord in matching_chords:
                if set(matching_chord) == set(chord):
                    matching_chords_checked.append(chord)
        matching_chords_checked.append(previous_event_chord)

        if self._matched_chord == []:
            matching_chords_checked = matching_chords

        print(self.event_group.measure, self.global_index, matching_chords_checked)

        min_dissonance = len(self._pitch_classes) + 1
        for chord in matching_chords_checked:
            dissonance = set(self._pitch_classes) - set(chord)
            if len(dissonance) <= min_dissonance:
                self._matched_chord = [self.resolve_base_chord(chord)]
                min_dissonance = len(dissonance)
        return

    def resolve_seventh(self, Flow):
        """ resolve seventh chord by finding the seventh chord and check with modulation"""
        if self._matched_chord == []:
            return

        seventh_chords = Flow.find_seven_chord(self._matched_chord[0])
        if seventh_chords == []:
        # Skip if no seventh chord
            return
        for seventh_chord in seventh_chords:
            seventh_note = list(set(seventh_chord) - set(self._matched_chord[0]))

            if seventh_note == []:
            # Skip if no seventh note found
                continue

            if seventh_note[0] not in self._pitch_classes:
            # Skip if not contained in corrected_pitch_class
                continue

            result = Flow.compare_chords(",".join(self._matched_chord[0]),",".join(seventh_chord))
            if result is None:
            # Return if no flow found
                continue

            if self._key in result:
                self._matched_chord = [self.resolve_base_chord(seventh_chord)]
                self._event_group.add_candidate_chord(seventh_chord, self._event_index)
                self._dissonance = [pitch for pitch in self._pitch_classes if pitch not in self._matched_chord[0]]
                return

    def resolve_dissonance(self):
        """find dissonance by eliminate matched chord pitch classes"""
        if len(self._matched_chord) > 0:
            # print(self._pitch_classes, self._matched_chord)
            self._dissonance = [pitch for pitch in self._pitch_classes if pitch not in self._matched_chord[0]]

            if self._event_index > 0:
                # Check if common dissonance exists in two measure
                previous_event = self._event_group.events[self._event_index-1]
                common_dissonances = set(self._dissonance) & set(previous_event._dissonance)

                if len(common_dissonances) != 0:
                    # Eliminate common dissonance based on candidate chord
                    chord_list = self._event_group.candidate_chords
                    for dissonance in common_dissonances:
                        new_list = []
                        for chord in chord_list:
                            if dissonance in chord[0]:
                                new_list.append(chord)
                        chord_list = new_list

                    if len(chord_list) != 0:
                        # Fix dissonance of previous event
                        for chord in chord_list:
                            dissonance = [pitch for pitch in previous_event._pitch_classes if pitch not in chord[0]]
                            if len(dissonance) <= len(previous_event._dissonance):
                                previous_event._matched_chord = [chord[0]]
                                previous_event._dissonance = dissonance
                # End of Common Dissonance

                # Change current chord if previous chord helps eliminate more dissonance
                dissonance = [pitch for pitch in self._pitch_classes if pitch not in previous_event._matched_chord[0]]
                if len(dissonance) <= len(self._dissonance):
                    self._matched_chord = previous_event._matched_chord
                    self._dissonance = [pitch for pitch in self._pitch_classes if pitch not in self._matched_chord[0]]

    def resolve_inversion(self):
        result = []
        for chord in self._matched_chord:
            result.append(self.resolve_base_chord(chord))
        self._matched_chord = result

    def print_out(self):
        joined_chords = ["".join(x) for x in self._matched_chord]
        logger.info("\tEvent: {} {}\tPitches: {}\tStep2 Pitches: {}\tChord: {}\tDissonance: {}\t".format(self._global_index, self._offset, "".join(self._pitch_classes), "".join(self._corrected_pitch_classes), joined_chords, self._dissonance))

class EventGroup:
    @property
    def candidate_chords(self):
        return self._candidate_chords

    @property
    def partial_candidate_chords(self):
        return self._partial_candidate_chords

    @property
    def measure(self):
        """int: the measure to which the group belong"""
        return self._measure

    @measure.setter
    def measure(self, value):
        self._measure = value

    @property
    def events(self):
        """list(Event): a list of event object belong to"""
        return self._events

    @property
    def number_of_events(self):
        """int: total number of events"""
        return self._number_of_events

    @number_of_events.setter
    def number_of_events(self, value):
        self._number_of_events = value

    def __init__(self):
        self._events = []
        self._measure = -1
        self._candidate_chords = []
        self._partial_candidate_chords = []

    def acoustic_lasting(self):
        """step 2 of event analyzer"""
        for i in range(self._number_of_events):
            if self._number_of_events == 1:
                self._events[i].corrected_pitch_classes += self._events[i].pitch_classes_octave
            else:
                if i == 0:
                    self._events[i].corrected_pitch_classes += self._events[i].pitch_classes_octave
                    self._events[i].corrected_pitch_classes += self._events[i+1].pitch_classes_octave

                elif i == self._number_of_events - 1:
                    self._events[i].corrected_pitch_classes += self._events[i].pitch_classes_octave
                    self._events[i].corrected_pitch_classes += self._events[i-1].pitch_classes_octave
                else:
                    self._events[i].corrected_pitch_classes += self._events[i+1].pitch_classes_octave
                    self._events[i].corrected_pitch_classes += self._events[i].pitch_classes_octave
                    self._events[i].corrected_pitch_classes += self._events[i-1].pitch_classes_octave

            self._events[i].corrected_pitch_classes = self.sort_single_event_notes(self._events[i].corrected_pitch_classes)
            self._events[i].corrected_pitch_classes = remove_identical(self._events[i].corrected_pitch_classes)

    def exact_match(self, Flow):
        """step 3 of event analyzer"""
        for event in self._events:
            event.match_triad_chord(Flow)

    def match_candidates(self):
        """step 4 of event analyzer"""
        for event in self._events:
            event.match_candidates()

    def match_containing(self, Flow):
        """step 5"""
        for event in self._events:
            event.match_candidates()
            event.match_subset(Flow)

    def match_partial(self, Flow):
        """step 6 of event analyzer (partial match)"""
        for event in self._events:
            event.match_partial(Flow)
        pass

    def select_chord(self, modulation):
        """ select chord """
        for event in self._events:
            event.select_chord(modulation)

    @staticmethod
    def find_bass_note(note_tuple):
        lowest_octave = min(note_tuple, key=lambda t: t[1])[1]
        lowest_octave_note = [note for note in note_tuple if note[1] == lowest_octave]
        bass_note = min(lowest_octave_note, key=lambda t: Interval.letter_to_pitch_number(t[0]))
        return bass_note

    @staticmethod
    def sort_single_event_notes(single_event):
        dict = {}
        for event in single_event:
            if event[1] not in dict:
                dict[event[1]] = []
            dict[event[1]].append(event[0])
        for key in dict:
            dict[key] = sorted(dict[key], key=lambda t:Interval.letter_to_pitch_number(t[0]))
        result = []
        for key in sorted(dict):
            result = result + dict[key]
        return result

    def resolve_chord_conflict(self, Flow, modulation):
        """ Resolve Problem to immediate exact chord match and the result match in step 5"""
        for event in self._events:
            event.resolve_chord_conflict(Flow, modulation)

    def resolve_seventh(self, Flow):
        " Find if seventh exist in the chord "
        for event in self._events:
            event.resolve_seventh(Flow)

    def resolve_dissonance(self):
        """Last step: find dissonance of all events belong to self"""
        for event in self._events:
            event.resolve_dissonance()

    def resolve_inversion(self):
        """ Resolve the inversion of the output """
        for event in self._events:
            event.resolve_inversion()

    def display(self):
        """show result"""
        # for clearer presentation
        joined_candidates = [",".join(x[0]) for x in self._candidate_chords]

        logger.info("Measure: {} no. of events: {} candidates: {}".format(self._measure, self._number_of_events, joined_candidates))
        # logger.info("Measure: {} no. of events: {}".format(self._measure, self._number_of_events))
        for event in self._events:
            event.print_out()

    def add_candidate_chord(self, list, offset):
        """
        add candidate chord
        :param list: a list of pitch classes of chord
        :return:
        """
        for chord in self._candidate_chords:
            if set(list) == set(chord[0]):
                return

        self._candidate_chords.append((list, offset))

    def add_partial_candidate_chord(self, list):
        """
        add partial candidate chord
        :param list: a list of pitch classes of chord
        :return:
        """
        for chord in self._partial_candidate_chords:
            if set(list) == set(chord):
                return

        self._partial_candidate_chords.append(list)

    def lazy_delete_duplicated_chords(self):
        first_encounter = []
        for event in self._events:
            if first_encounter == event.matched_chord:
                event.duplicated = True
            else:
                first_encounter = event.matched_chord
        pass

class EventContainer:
    @property
    def all_dissonances(self):
        dissonances = []
        for event_group in self._event_groups:
            diss = []
            for event in event_group:
                diss.append(event.dissonance)
            dissonances.append(diss)

    @property
    def events(self):
        events = []
        for event_group in self._event_groups:
            for event in event_group.events:
                events.append(event)
        return events

    @property
    def number_of_events(self):
        return len(self.events)

    def get_event_at(self, global_index):
        return self.events[global_index]

    def get_analysis_result(self):
        output_list = []
        for event in self.events:
            output_dict = {}
            if not event.matched_chord:
                output_dict['chord'] = "n/a"
            else:
                output_dict['chord'] = event.matched_chord[0]

            output_dict['index'] = event.global_index
            output_dict['pitches'] = event.pitch_classes

            output_list.append(output_dict)

        return output_list

    def events_between(self, starting_measure, starting_offset, ending_measure, ending_offset):
        """measure starts from 1"""
        output_events = []
        for i in range(starting_measure - 1, ending_measure - 1 + 1):
            for event in self.event_groups[i].events:
                if i == starting_measure - 1:
                    if i == 0 and event.offset >= starting_offset:
                        output_events.append(event)
                    elif i != 0 and event.offset > starting_offset:
                        output_events.append(event)
                elif i == ending_measure - 1:
                    if event.offset < ending_offset and ending_offset != 0:
                        output_events.append(event)
                else:
                    output_events.append(event)
        return output_events
    @property
    def event_groups(self):
        """list(EventGroup): a list of (EventGroup) references"""
        return self._event_groups

    @property
    def chord_data(self):
        """Dict: all chord data for matching"""
        return self._chord_data

    def __init__(self):
        self._event_groups = []
        self._chord_data = MusicManager.get_instance().make_chord_database()

    def display(self):
        """display result"""
        for event_group in self._event_groups:
            event_group.display()

    def output_to_chord_flow_old(self):
        """output result in chord list format"""
        score = []
        for group in self._event_groups:
            measure = []
            measure.append(group.number_of_events)
            for event in group.events:
                measure.append(''.join(event.matched_chord))
            score.append(measure)

        return score

    def lazy_delete_duplicated_chord(self):
        for group in self._event_groups:
            group.lazy_delete_duplicated_chords()

if __name__ == "__main__":
    pass