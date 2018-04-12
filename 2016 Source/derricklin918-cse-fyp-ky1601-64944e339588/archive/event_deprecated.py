# ===================
# module: event.py
# description: TODO
# ===================
import logging
import os

from pianoreduction.recognition.eventanalysis.lib import MusicManager, Interval
from pianoreduction import config

# ===== logger setting =====
log_file_name = "event_analyzer.log"
log_file_path = os.path.join(config.LOG_DIR, log_file_name)

logger = logging.getLogger("Analyzer")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
file = logging.FileHandler(log_file_path, mode = 'w')
file.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(name)s %(levelname)s %(message)s")
ch.setFormatter(formatter)

# on/off for console log and file log
logger.addHandler(ch)
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
        self._duplicated = False

    def resolve_base_chord(self, matched_chord):
            result = []
            for pitch in self._corrected_pitch_classes:
                if pitch in matched_chord:
                    result.append(pitch)
            for pitch in matched_chord:
                if pitch not in self._corrected_pitch_classes:
                    result.append(pitch)
            return result


    def resolve_base_problem(self, matched_chords):
        result = []
        for chord in matched_chords:
            result.append(self.resolve_base_chord(chord))
        return result


    def match_triad_chord(self, Flow):
        """
        Match corrected pitch classes against chord data list
        Args:
            None
        Return:
            None
        """
        if (Flow.match_chord_exact(self._corrected_pitch_classes) and len(self._corrected_pitch_classes) == 3):
            self._is_chord_match = True
            self._matched_chord.append(self._corrected_pitch_classes)
            self._event_group.add_candidate_chord(self._corrected_pitch_classes, self.event_index)
            return


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

    def match_using_flow(self, Flow, chord=[]):
        # find previous chord
        i = self.find_previous_chord(chord)
        if (i == -1):
            return
        previous_chord = self._event_container.events[self._global_index - i].matched_chord
        previous_chord_key = [",".join(x) for x in previous_chord]

        # find second previous chord
        previous_second_chord = []
        previous_second_chord_key = []
        j = self.find_previous_chord(previous_chord[0], i)
        if j != -1:
            previous_second_chord = self._event_container.events[self._global_index - j].matched_chord
            previous_second_chord_key = [",".join(x) for x in previous_second_chord]
        dict = {}
        if previous_second_chord != []:
            # get previous flow
            result_chord = []
            previous_flow_result = Flow.compare_chords(previous_second_chord_key[0], previous_chord_key[0])
            if previous_flow_result is not None:
                for flow in previous_flow_result:
                    dict[flow[0] + '-' + flow[1]] = flow[4]
            # print("DICT:", self._event_group.measure, self._global_index, previous_second_chord_key[0], previous_chord_key[0], dict)

        result_chord = []
        maximum_weight = -100
        for chord in self._matched_chord:
            flow_results = []
            if previous_chord is not None:
                flow_results = Flow.compare_chords(previous_chord_key[0], ",".join(chord))
                # print("FLOW:", self._event_group.measure, self._global_index, chord, dict, flow_results)
                if flow_results is not None:
                    flow_results_modified = [flow for flow in flow_results if flow[0] + '-' + flow[1] in dict]
                    if dict == {}:
                        flow_results_modified = flow_results
                    if flow_results_modified == []:
                        continue
                    maximum_local_weight = max(flow_results_modified, key=lambda t: t[4])
                    if (maximum_weight < maximum_local_weight[4]):
                        result_chord = [self.resolve_base_chord(chord)]
                        maximum_weight = maximum_local_weight[4]
                        maximum_key = (maximum_local_weight[0], maximum_local_weight[1])

        # flows_fixed = [x for x in flows if x is not None]
        if result_chord != []:
            self._matched_chord = result_chord
            self._event_group.add_candidate_chord(result_chord[0], self.event_index)
            self._is_chord_match = True

    def match_subset(self, Flow):
        if len(self._corrected_pitch_classes) > 3 and self._is_chord_match is False:
            chord_subsets = Flow.match_chord_subset(self._corrected_pitch_classes)
            self._matched_chord += self.resolve_base_problem(chord_subsets)
            # print("SUBSET: ", self._event_group.measure, self._global_index, self._matched_chord, self._corrected_pitch_classes)

            # if len(self._matched_chord) == 1:
            #     self._event_group.add_candidate_chord(self._matched_chord[0], self.event_index)
            #     self._is_chord_match = True
            #
            # elif len(self._matched_chord) > 1:
            if len(self._matched_chord) != 0:
                self.match_using_flow(Flow)


    def match_partial(self, Flow):
        if self._is_chord_match is False:
            chord_partials = Flow.match_chord_partial(self._corrected_pitch_classes)
            self._matched_chord += self.resolve_base_problem(chord_partials)
            if len(self._matched_chord) != 0:
                self.match_using_flow(Flow)

    def match_candidates(self):
        # if the event is not matched to a chord
        if self._is_chord_match == False:
            # for each chord candidate, try matching triads with at least two and three pitches are the same
            candidate_list = []
            for candidate in self._event_group.candidate_chords:
                # print(candidate)
                p = set(candidate[0]) & set(self._corrected_pitch_classes)
                if len(candidate[0]) - len(p) <= 1:
                    if len(candidate[0]) == 3 or len(candidate[0]) == 4:
                        candidate_list.append(candidate)
            if candidate_list != []:
                # Get the closest_candidate to the chord
                # print("CANDIDATE: ",self._event_group.measure, self._global_index,  self._corrected_pitch_classes, candidate_list)
                closest_candidate = min(candidate_list, key=lambda t:abs(t[1] - self.event_index))[0]
                self._matched_chord = [self.resolve_base_chord(closest_candidate)]
                self._is_chord_match = True


            # # for each chord candidate, try matching triads with at least one pitches are the same
            # for candidate in self._event_group.candidate_chords:
            #     p = set(candidate) & set(self._corrected_pitch_classes)
            #     if len(candidate) - len(p) == 2 and len(candidate) == 3:
            #         self._matched_chord = candidate
            #         self._is_chord_match = True
            #         self._chord = Chord(self._matched_chord, self._bass_note)
            #         return

    def resolve_chord_conflict(self, Flow, all_modulations):
        """ Resolve the chord conflict on immediate chord by checking similarity"""
        if all_modulations is None:
            return
        if Flow.match_chord_exact(self._pitch_classes):
            chord = self._pitch_classes
            if self._matched_chord != [] and set(chord) == set(self._matched_chord[0]):
                # return if it is already the matched chord
                return
            if len(self._pitch_classes) == 4:
                chord = Flow.remove_seven_chord(self._pitch_classes)
            if self.backtrack_chord_conflict(chord, Flow, all_modulations):
                for event in self.event_group.events:
                    event.backtrack_chord_conflict(chord, Flow, all_modulations)


    def backtrack_chord_conflict(self, chord, Flow, all_modulations):
        """ Expand the result to other event, return true if chord changed"""
        if self._matched_chord != []:
            dissonance_immediate_chord = set(self._corrected_pitch_classes) - set(chord)
            dissonance_matching_chord = set(self._corrected_pitch_classes) - set(self._matched_chord[0])
            # print("Resolving CC: ", self.event_group.measure, self._global_index, self._corrected_pitch_classes, self._pitch_classes, dissonance_immediate_chord, self._matched_chord[0], dissonance_matching_chord)
            if len(dissonance_immediate_chord) < len(dissonance_matching_chord):
        # change matched chord if immediate chord has higher similarity to the corrected pitch class
                self._matched_chord = [self.resolve_base_chord(chord)]
                return self.resolve_chord_conflict_by_modulation(chord,Flow, all_modulations)
            elif len(dissonance_immediate_chord) == len(dissonance_matching_chord):
                self._matched_chord.append(self.resolve_base_chord(chord))
                # print("BACKTRACK CC:", self._event_group.measure, self._global_index,self._matched_chord, chord)
                return self.resolve_chord_conflict_by_modulation(chord, Flow, all_modulations)
        return False

    def resolve_chord_conflict_by_modulation(self, immediate_chord, Flow ,all_modulations):
        previous_modulation = []
        current_modulation = []
        for modulation in all_modulations:
            if modulation[0] > self._event_group.measure:
                current_modulation = modulation
                break
            elif modulation[0] == self._event_group.measure and modulation[1] >= self._offset:
                current_modulation = modulation
                break
            previous_modulation = modulation

        # print("RESOLVE CC MODULATION:", self._event_group.measure, self._global_index, previous_modulation, current_modulation)

        if current_modulation != []:
            key = current_modulation[2] + '-'
            key = key + 'Major' if current_modulation[-1] else key + 'Minor'
        elif previous_modulation != []:
            key = previous_modulation[2] + '-'
            key = key + 'Major' if previous_modulation[-1] else key + 'Minor'
        else:
            # return if no modulation
            return False

        i = self.find_previous_chord(self._matched_chord[0])
        j = self.find_previous_chord(immediate_chord)
        if j > i:
            i = j
        if (i == -1):
            return False
        previous_chord = self._event_container.events[self._global_index - i].matched_chord
        previous_chord_key = [",".join(x) for x in previous_chord]

        # print("RESOLVE CC KEY:", self._event_group.measure, self._global_index, previous_chord, previous_chord_key)

        result_chord = []
        maximum_weight = -100
        for chord in self._matched_chord:
            if previous_chord is not None:
                flow_results = Flow.compare_chords(previous_chord_key[0], ",".join(chord))
                # print("RESOLVE FLOW: ",self._event_group.measure, self._global_index, chord, flow_results)
                if flow_results is not None:
                    flow_results_modified = [flow for flow in flow_results if flow[0] + '-' + flow[1] == key]
                    if flow_results_modified == []:
                        continue
                    maximum_local_weight = max(flow_results_modified, key=lambda t: t[4])
                    if (maximum_weight < maximum_local_weight[4]):
                        result_chord = [self.resolve_base_chord(chord)]
                        maximum_weight = maximum_local_weight[4]

        self._matched_chord = result_chord
        if result_chord != []:
            self._event_group.add_candidate_chord(result_chord[0], self.event_index)
            self._is_chord_match = True
            if result_chord[0] == immediate_chord:
                return True
        return False

    def resolve_seventh(self, Flow, all_modulations):
        """ resolve seventh chord by finding the seventh chord and check with modulation"""
        if self._matched_chord == []:
        # return if no matched chord
            return
        seventh_chords = Flow.find_seven_chord(self._matched_chord[0])
        for seventh_chord in seventh_chords:
            seventh_note = list(set(seventh_chord) - set(self._matched_chord[0]))

            if seventh_note == []:
                # Skip if no seventh note found
                continue

            if seventh_note[0] not in self._corrected_pitch_classes:
                # Skip if not contained in corrected_pitch_class
                continue

            if self.resolve_seventh_by_modulation(seventh_chord, seventh_note[0],all_modulations):
                return

    def resolve_seventh_by_modulation(self, chord, seventh_note, all_modulations):
        previous_modulation = []
        current_modulation = []
        for modulation in all_modulations:
            if modulation[0] > self._event_group.measure:
                current_modulation = modulation
                break
            elif modulation[0] == self._event_group.measure and modulation[1] >= self._offset:
                current_modulation = modulation
                break
            previous_modulation = modulation

        # print("MODULATION: " , self._event_group.measure, self._global_index, chord, self._matched_chord, self._offset, current_modulation, previous_modulation)

        # Check the modulation from the current chord
        if current_modulation != []:
            chord_dict = MusicManager.get_instance().make_dict(current_modulation[2], current_modulation[-1])
            if ",".join(chord) in chord_dict:
                self._matched_chord = [self.resolve_base_chord(chord)]
                for event in self.event_group.events:
                    event.backtrack_seventh_chord(chord, seventh_note)
                return True

        # Check the modulation to the current chord
        if previous_modulation != []:
            chord_dict = MusicManager.get_instance().make_dict(previous_modulation[2], previous_modulation[-1])
            if ",".join(chord) in chord_dict:
                self._matched_chord = [self.resolve_base_chord(chord)]
                for event in self.event_group.events:
                    event.backtrack_seventh_chord(chord, seventh_note)
                return True

        return False

    def backtrack_seventh_chord(self, chord, seventh_note):
        """backtrack the seventh chord resolved if it resolves more dissonance"""
        # if seventh_note not in self._pitch_classes:
        #     # Skip when seventh note not in self._pitch_class
        #     return
        if self._matched_chord != []:
            dissonance_immediate_chord = set(self._pitch_classes) - set(chord)
            dissonance_matching_chord = set(self._pitch_classes) - set(self._matched_chord[0])
            # print("BackTrack: ", self.event_group.measure, self._global_index, self._corrected_pitch_classes, self._pitch_classes, dissonance_immediate_chord, self._matched_chord[0], dissonance_matching_chord)
            if len(dissonance_immediate_chord) <= len(dissonance_matching_chord):
            # change matched chord if immediate chord has higher similarity to the corrected pitch class
                self._matched_chord = [self.resolve_base_chord(chord)]


    def resolve_dissonance(self):
        """find dissonance by eliminate matched chord pitch classes"""
        if len(self._matched_chord) > 0:
            # print(self._pitch_classes, self._matched_chord)
            self._dissonance = [pitch for pitch in self._pitch_classes if pitch not in self._matched_chord[0]]
        else:
            # find previous chord if no chord find
            previous_dissonance = self._pitch_classes
            next_dissonance = self._pitch_classes
            i = self.find_previous_chord()
            if(i != -1):
                previous_dissonance = [pitch for pitch in self._pitch_classes if pitch not in self._event_container.events[self._global_index - i].matched_chord[0]]
            i = self.find_next_chord()
            if (i != -1):
                next_dissonance = [pitch for pitch in self._pitch_classes if pitch not in self._event_container.events[i].matched_chord[0]]
            if len(previous_dissonance) > len(next_dissonance):
                self._dissonance = next_dissonance
            else:
                self._dissonance = previous_dissonance



    def print_out(self):
        joined_chords = ["".join(x) for x in self._matched_chord]
        logger.debug("\tEvent: {} {}\tPitches: {}\tStep2 Pitches: {}\tChord: {}\tDissonance: {}\t".format(self._global_index, self._offset, "".join(self._pitch_classes), "".join(self._corrected_pitch_classes), joined_chords, self._dissonance))

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
            event.match_candidates()
            event.match_partial(Flow)
        pass

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
            # print(key, dict[key])
        result = []
        for key in sorted(dict):
            result = result + dict[key]
        # print(result)
        return result

    def resolve_chord_conflict(self, Flow, modulation):
        """ Resolve Problem to immediate exact chord match and the result match in step 5"""
        for event in self._events:
            event.resolve_chord_conflict(Flow, modulation)

    def resolve_seventh(self, Flow, modulation):
        " Find if seventh exist in the chord "
        if modulation != []:
            for event in self._events:
                event.resolve_seventh(Flow, modulation)

    def resolve_dissonance(self):
        """Last step: find dissonance of all events belong to self"""
        for event in self._events:
            event.resolve_dissonance()

    def display(self):
        """show result"""
        # for clearer presentation
        joined_candidates = [",".join(x[0]) for x in self._candidate_chords]

        logger.debug("Measure: {} no. of events: {} candidates: {}".format(self._measure, self._number_of_events, joined_candidates))
        # logger.debug("Measure: {} no. of events: {}".format(self._measure, self._number_of_events))
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