import logging
import os
from itertools import permutations, combinations, groupby

from pyexcel_xlsx import get_data

from pianoreduction import config
from pianoreduction.recognition.eventanalysis.lib import MusicManager

# ===== logger setting =====
log_file_name = "chord_flow.log"
log_file_path = os.path.join(config.LOG_DIR, log_file_name)

logger = logging.getLogger("Flow")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(name)s %(levelname)s %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

file = logging.FileHandler(log_file_path, mode = 'w')
file.setLevel(logging.INFO)

logger.addHandler(file)
logger.propagate = False
# ===== logger setting end =

data_path = os.path.join(config.DATA_DIR, "recognition_model")

class FlowState:

    all_pitch = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    @property
    def map(self):
        return self._map

    @property
    def weight(self):
        return self._majweight

    @property
    def sheet_major(self):
        return self._major

    @property
    def sheet_minor(self):
        return self._minor




    def __init__(self):

        # Path
        major_path = os.path.join(data_path, "Chord Flow - Major keys.xlsx")
        minor_path = os.path.join(data_path, "Chord Flow - Minor keys.xlsx")
        major_weight_path = os.path.join(data_path, "major_flow_weight.xlsx")
        minor_weight_path = os.path.join(data_path, "minor_flow_weight.xlsx")

        # Get major data
        self._major = get_data(major_path, start_row=1)["Sheet1"]
        self._majweight = get_data(major_weight_path, start_row=1)["Sheet1"]
        # TODO: now just append a None to the last element to fix the list size. need better solution
        self._major[len(self._major)-1].append(None)

        # Get minor data
        self._minor = get_data(minor_path, start_row=1)["Sheet1"]
        self._minweight = get_data(minor_weight_path, start_row=1)["Sheet1"]
        self._minor[len(self._minor) - 1].append(None)

        # Create major and minor index
        self._major_index = []
        self._minor_index = []
        self._map = {}
        self._seven = {}
        for row in self._major:
            self._major_index.append(row[0])
        for row in self._minor:
            self._minor_index.append(row[0])

        chord_list = MusicManager.get_instance().make_table_full_extend()
        self.make_map(chord_list[0], "Major", self._major_index, self._majweight)
        self.make_map(chord_list[1], "Minor", self._minor_index, self._minweight)

                            # map data structure: dict(index)-> dict(target index)
                            # -> list(list(pitch, Maj/Min, index roman, target roman, weight))
                            # e.g {'CEG' : { 'GBD' : [['C', 'Major', 'I', 'V', -0.856126], ['G', 'Major', 'IV', 'I', -1.111717], ...], ...}, ...}

    def print_sheet(self):
        print("major: ", self._major)
        print("index: ", self._major_index)
        print("minor: ", self._minor)
        print("index: ", self._minor_index)

    def match_chord_exact(self, input_list):
        # Found exact match chord including inversion
        input_copy = input_list
        for permutated_input in permutations(input_copy):
            key = ",".join(permutated_input)
            if key in self._map:
                return True
        return False

    def match_chord_subset(self, input_list):
        # Found exact match chord from the subset of input
        input_copy = input_list
        output_list = []
        combination_list = list(combinations(input_copy, 3)) + list(combinations(input_copy, 4))
        for com in combination_list:
            key = ",".join(com)
            if key in self._map:
                output_list.append(list(com))
        return output_list

    def match_chord_partial(self, input_list):
        # Found partial match from chord containing 2 or 3 equal note
        output_list = []
        for pitch in MusicManager.all_pitch_class:
            if pitch not in input_list:
                input = [pitch] + input_list
                output_list = output_list + self.match_chord_subset(input)
        # Use function to convert to chord without inversion
        eliminated_inversion_output = [self.eliminate_inversion(chord) for chord in output_list]
        return self.remove_duplicate(eliminated_inversion_output)

    def remove_duplicate(self, input_list):
        input = sorted(input_list)
        return list(input for input,_ in groupby(input))

    def eliminate_inversion(self, input_list):
        # Change the permutation of note to roman without inversion
        input_copy = input_list
        output_list = []
        for permutated_chord in permutations(input_copy):
            key = ",".join(permutated_chord)
            if(key in self._map):
                index = list(self._map[key].keys())[0]
                music_key = list(self._map[key][index].keys())[0]
                roman = self._map[key][index][music_key][0]
                # Check whether 6 or 4 exist in roman
                if('6' not in roman and '4' not in roman):
                    output_list = list(permutated_chord)
        return output_list

    def add_seven_chord(self, input_list):

        key = ",".join(input_list[:3])

        if key not in self._seven:
            self._seven[key] = [input_list]
            return

        for seven_chord in self._seven[key]:
            if set(seven_chord) == set(input_list):
                return
        self._seven[key].append(input_list)

    def find_seven_chord(self, input_list):
        output_list = []
        input_copy = input_list
        for permutated_list in permutations(input_copy):
            key = ",".join(permutated_list)
            if key in self._seven:
                output_list = output_list + self._seven[key]
        return output_list

    def remove_seven_chord(self, input_list):
        output_list = []
        input_copy = input_list
        for combinated_list in combinations(input_copy, 3):
            current = list(combinated_list)
            for output in self.find_seven_chord(current):
                if set(output) == set(input_list):
                    output_list.append(current)
                    break

        if output_list != []:
            return output_list
        return [input_list]

    def print_map(self):
        for key in self._map:
            print("MAP(",key,"): ", self._map[key])

    def chord_convert(self, chord):
        result = []
        for note in chord:
            result.append(self.note_convert(note))
        return result

    def note_convert(self, note):
        if len(note) == 1:
            return note
        index = self.all_pitch.index(note[0])
        for words in note[1:]:
            if words == '#':
                index = index+1
            elif words == '-':
                index = index-1
        length = len(self.all_pitch)
        if index >= length:
            index = index % length
        if index < 0:
            index = length + index
        return self.all_pitch[index]

    def key_exist(self, key):
        if key in self._map:
            return True
        else:
            return False

    def check_missing_chord(self):
        all_chords = MusicManager.get_instance().make_chord_database()
        count = 0
        for chord in all_chords:
            output_chord = ",".join(chord)
            if output_chord not in self._map:
                print("Missing Chord: ", output_chord)
                count+=1
        print("Total Missing Chord: ",count)

    def make_map(self, chord_list, quality, index_list, weight_list):

        # Make major chord flow
        for pitch in MusicManager.all_pitch_class:
            for i in range(0,len(chord_list[pitch])):
                current = index_list.index(chord_list[pitch][i][1])   # current index no.

                if len(chord_list[pitch][i][0]) == 4:
                    self.add_seven_chord(chord_list[pitch][i][0])

                for roman in chord_list[pitch]:
                    target = index_list.index(roman[1])  # target index no.
                    # if(self._major[current][target+1] == "Yes"):
                    # Generate all permutations of chord with inversion (index)
                    for index_part in permutations(chord_list[pitch][i][0][1:]):
                        index = chord_list[pitch][i][0][0]+","+",".join(index_part)
                        if index not in self._map:
                            self._map[index] = {}
                        # Generate all permutations of chord with inversion (target)
                        for target_part in permutations(roman[0][1:]):
                            target_index = roman[0][0]+","+",".join(target_part)
                            if target_index not in self._map[index]:
                                self._map[index][target_index] = {}
                            if index_list[current] == roman[1]:
                                self._map[index][target_index][pitch + "," + quality] = [index_list[current], roman[1], 0]
                            else:
                                self._map[index][target_index][pitch+ "," + quality] = [index_list[current], roman[1], weight_list[current][target+1]]
        # for key in self._map:
        #     print("Map: ", key, self._map[key])


    def compare_chords(self, current, next):
        # compare two key and output the possible flow
        if current in self._map:
            if next in self._map[current]:
                logger.debug("OUTPUT: {} {} {}".format(current, next, self._map[current][next]))
                return self._map[current][next]
        logger.debug("OUTPUT: {} {} {}".format(current, next, None))

    def compare_events(self, current_event, next_event):
        # compare two events and output the possible flow
        if current_event.output_chord in self._map:
            if next_event.output_chord in self._map[current_event.output_chord]:
                logger.debug("OUTPUT: {} {} {} {}".format(current_event.offset, current_event.output_chord, next_event.output_chord, self._map[current_event.output_chord][next_event.output_chord]))

    def get_chord_flow_results(self, current_event, next_event):
            if current_event.chord in self._map:
                if next_event.chord in self._map[current_event.chord]:
                    logger.debug("Measure: {}\tOffset: {} {} {} {}".format(current_event.event_group.measure, current_event.offset, current_event.chord,
                                                             next_event.chord,
                                                             self._map[current_event.chord][next_event.chord]))
                    if set(current_event.matched_chord[0]) != set(next_event.matched_chord[0]):
                        # Prevent chord flow between inversion on lyrics
                        return self._map[current_event.chord][next_event.chord]

    def unequal_matched_chord_event(self, current_event, next_event):
        if current_event.matched_chord == [] or next_event.matched_chord == []:
            return False
        if len(current_event.matched_chord) != len(next_event.matched_chord):
            return True
        else:
            i = 0
            for current_chord in current_event.matched_chord:
                for next_chord in next_event.matched_chord:
                    if set(current_chord) == set(next_chord):
                        i = i+1
            if i == len(current_event.matched_chord):
                return False
            else:
                return True


    def get_event_all_flow_results(self, current_event, next_event):
        output_full_list = []
        for current_chord in current_event.matched_chord:
            current_chord_key = ",".join(self.eliminate_inversion(current_chord))
            current_dict = {}
            for next_chord in next_event.matched_chord:
                next_chord_key = ",".join(self.eliminate_inversion(next_chord))
                flow_result = self.compare_chords(current_chord_key, next_chord_key)
                if flow_result != None:
                    for key in flow_result:
                        weight = flow_result[key][2]
                        if key not in current_dict:
                            current_dict[key] = [next_chord_key, weight, flow_result[key][0], flow_result[key][1]]
                        elif current_dict[key][1] < weight:
                            current_dict[key] = [next_chord_key, weight, flow_result[key][0], flow_result[key][1]]
            output_full_list.append((current_chord_key, current_dict))
        return output_full_list

    @staticmethod
    def get_max_key(output_list, start_position, Num_of_Flow, start_chord = None):
        """ obtain the common key of the event_list
            input : [ measure, offset,
                        [
                            ('First From', {'Key':['NEXT CHORD' , Weight] ...}),
                            ('Second From', {'Key':['NEXT CHORD' , Weight] ...})
                            ...
                        ]
                    ] ...
            :return { 'Key': Weight ... }
        """
        max_key = ''
        weight = 0
        next_chord = ''
        for length in reversed(range(0, Num_of_Flow)):
            if max_key != '':
            # Break if result found
                break

            end = start_position+1
            while end < len(output_list):
                if output_list[start_position][0] + length >= output_list[end][0]:
                    end = end + 1
                else:
                    break
            # print(start_position, end, length)

            # Prepare list for checking
            check_list = output_list[start_position:end]

            # Find The Weight of each key
            if start_chord is not None:
                # Next_chord provided
                for key in start_chord[1]:
                    current_weight = FlowState.get_common_key_by_flow_statistic(check_list, start_chord[0].split(','), key)
                    if current_weight != None:
                        if current_weight > weight or max_key == '':
                            max_key = key
                            weight = current_weight
                            next_chord = start_chord[0]
            else:
                # Next_chord not provided
                for matched_chords_flow in check_list[0][2]:
                    for key in matched_chords_flow[1]:
                        current_weight = FlowState.get_common_key_by_flow_statistic(check_list, matched_chords_flow[0].split(','), key)
                        if current_weight != None:
                            if current_weight > weight or max_key == '':
                                max_key = key
                                weight = current_weight
                                next_chord = matched_chords_flow[0]
        # End of For Loop

        return (max_key, next_chord)

    @staticmethod
    def get_common_key_by_flow_statistic(output_list, next, key):
        """ Scan through the """
        next_chord = next
        max_key = key
        weight = 0

        for event in output_list:
            for matched_chords_flow in event[2]:
                current_chord = matched_chords_flow[0].split(',')
                if set(current_chord) == set(next_chord):
                    if max_key not in matched_chords_flow[1]:
                        return
                    else:
                        next_chord = matched_chords_flow[1][max_key][0].split(',')
                        weight = weight + matched_chords_flow[1][max_key][1]
                    break
        # print("CORR:", next, key, weight)
        return weight

    def modulation_process(self, output_list, next, key, Num_of_Flow, tolerance):
        # main process of modulation, process through the path
        modulation = []
        next_chord = next
        max_key = key
        weight = 0

        for event in output_list:
            for matched_chords_flow in event[2]:
                current_chord = matched_chords_flow[0].split(',')
                if set(current_chord) == set(next_chord):

                    if max_key not in matched_chords_flow[1] and matched_chords_flow != {}:
                        # Key Change
                        start = output_list.index(event)
                        max_key = FlowState.get_max_key(output_list, start, Num_of_Flow, matched_chords_flow)[0]
                        weight = 0
                        next_chord = []
                    # End of if

                    if max_key in matched_chords_flow[1]:
                        # Set Next Chord and Weight
                        next_chord = matched_chords_flow[1][max_key][0].split(',')
                        weight = weight + matched_chords_flow[1][max_key][1]
                        modulation.append([event[0], event[1], max_key, current_chord, next_chord, matched_chords_flow[1][max_key][2],matched_chords_flow[1][max_key][3], weight])

                    elif start < len(output_list)-1:
                        # NO FLOW BETWEEN
                        start = output_list.index(event)
                        Test = FlowState.get_max_key(output_list, start + 1, Num_of_Flow)
                        weight = 0
                        max_key = Test[0]
                        next_chord = Test[1].split(',')
                    # End of if

                    # print("KEY CHANGE", event[0], event[1], current_chord, next_chord, max_key, weight, matched_chords_flow[1])
                    if weight < tolerance:
                        max_key = ''
                    break

            if next_chord == [''] and start < len(output_list)-1:
                # NO FLOW BETWEEN
                start = output_list.index(event)
                Test = FlowState.get_max_key(output_list, start + 1, Num_of_Flow)
                weight = 0
                max_key = Test[0]
                next_chord = Test[1].split(',')
                # print("NO KEY: ", event[0], event[1], next_chord, max_key, event[2])

        return modulation

    def get_modulations(self, event_analyzer, Num_of_Flow = 4, tolerance = -0.5):
        """This function return the modulations of the given event_analyzer by comparing flows between chord """
        output_list = []
        events = event_analyzer.event_container.events
        before = events[0]

        for after in events:
            # Find First matched chord
            if after.matched_chord != []:
                before = after
                break
        if before.matched_chord == [] and before.global_index+1 >= len(events):
            # Skip if all chord is unmatched or before is last event
            return

        cached_flow = []

        for after in events[before.global_index+1:]:
            # Create output list
            if after.matched_chord != []:
                if self.unequal_matched_chord_event(before, after):
                    # print("UNMATCH: ", before.matched_chord, after.matched_chord)
                    list_of_possible_keys = self.get_event_all_flow_results(before, after)
                    output_list.append([before.event_group.measure, before.offset, list_of_possible_keys])
                    before = after
                    cached_flow = []
                elif len(before.matched_chord) != 1:
                    if cached_flow == []:
                        list_of_possible_keys = self.get_event_all_flow_results(before, after)
                        cached_flow = list_of_possible_keys
                    else:
                        list_of_possible_keys = cached_flow
                    output_list.append([before.event_group.measure, before.offset, list_of_possible_keys])
                    before = after
                else:
                    # print("SKIP: ",before.matched_chord, after.matched_chord)
                    cached_flow = []
                    before = after
        # output list structure: [measure, offset,
        #                           [
        #                               ('First From', {'Key': ['NEXT CHORD', Weight]}),
        #                               ('Second From', {'Key': ['NEXT CHORD', Weight]})
        #                               ...
        #                           ]
        #                       ]...

        # for event in output_list:
        # # Print output list
        #     print("EVENT: ",event[0], event[1])
        #     for matched_chords_flow in event[2]:
        #         print(" CHORD: ", matched_chords_flow[0])
        #         for key in matched_chords_flow[1]:
        #             print("     TO:", key, matched_chords_flow[1][key])

        if len(output_list) == 0:
            # Skip if no
            return

        # Find the initial next_chord and max_key
        Test = FlowState.get_max_key(output_list, 0, Num_of_Flow)
        max_key = Test[0]
        next_chord = Test[1].split(',')

        # Find the First NEXT CHORD using only max key and flow
        modulation = self.modulation_process(output_list, next_chord, max_key, Num_of_Flow, tolerance)

        for modulate in modulation:
            logger.debug("MODULATION: {}".format(modulate))

        return modulation

if __name__ == "__main__":
    s = FlowState()
    # s.print_map()
    print(s.compare_chords("C#,E,G","C#,B,E,G"))
    print(s.match_chord_subset(['D','G#','A','B','C']))
    print(s.find_seven_chord(['E', 'G#','B']))
    print(s.remove_seven_chord(['E', 'B', 'G#', 'C#']))
    print(s.match_chord_partial(['A', 'D', 'C']))
    print(s.eliminate_inversion(['A','C#','E']))
    print(s.match_chord_exact(['B','G#','C#','E']))



