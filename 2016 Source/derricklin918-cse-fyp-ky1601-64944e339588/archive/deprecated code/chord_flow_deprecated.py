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
file = logging.FileHandler(log_file_path, mode = 'w')
file.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(name)s %(levelname)s %(message)s")
ch.setFormatter(formatter)

# on/off for console log and file log
# logger.addHandler(ch)
# logger.addHandler(file)
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
        for row in self._major:
            self._major_index.append(row[0])
        for row in self._minor:
            self._minor_index.append(row[0])


        self.make_map()     # map data structure: dict(index)-> dict(target index)
                            # -> list(list(pitch, Maj/Min, index roman, target roman, weight))
                            # e.g {'CEG' : { 'GBD' : [['C', 'Major', 'I', 'V', -0.856126], ['G', 'Major', 'IV', 'I', -1.111717], ...], ...}, ...}

    def print_sheet(self):
        print("major: ", self._major)
        print("index: ", self._major_index)
        print("minor: ", self._minor)
        print("index: ", self._minor_index)

    def match_chord_exact(self, input_list):
        # Found exact match chord including inversion
        for permutated_input in permutations(input_list):
            key = ",".join(permutated_input)
            if key in self._map:
                return True
            else:
                return False

    def match_chord_subset(self, input_list):
        # Found exact match chord from the subset of input
        output_list = []
        combination_list = list(combinations(input_list, 3)) + list(combinations(input_list, 4))
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
        output_list = []
        for permutated_chord in permutations(input_list):
            key = ",".join(permutated_chord)
            if(key in self._map):
                index = list(self._map[key].keys())[0]
                roman = self._map[key][index][0][2]
                # Check whether 6 or 4 exist in roman
                if('6' not in roman and '4' not in roman):
                    output_list = list(permutated_chord)
        return output_list

    def find_seven_chord(self, input_list):
        output_list = []
        # find the seven chord of the input_list
        input = self.eliminate_inversion(input_list)
        for pitch in MusicManager.all_pitch_class:
            seven_input = self.eliminate_inversion(input + [pitch])
            if self.match_chord_exact(seven_input):
                if ",".join(input) in self._map[",".join(seven_input)]:
                    result = self._map[",".join(seven_input)][",".join(input)][0]
                    if result[3] in result[2]:
                        output_list.append(seven_input)
                        return output_list
        return output_list

    def remove_seven_chord(self, input_list):
        for combinated_list in combinations(input_list, 3):
            seven_chord = self.find_seven_chord(list(combinated_list))
            if seven_chord is not None:
                for chord in seven_chord:
                    if set(chord) == set(input_list):
                        return list(combinated_list)

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

    def make_map(self):

        # Obtain all chord
        chord_list = MusicManager.get_instance().make_table_full_extend()

        # Make major chord flow
        for pitch in MusicManager.all_pitch_class:
            for i in range(0,len(chord_list[0][pitch])):
                current = self._major_index.index(chord_list[0][pitch][i][1])   # current index no.
                for roman in chord_list[0][pitch]:
                    target = self._major_index.index(roman[1])                  # target index no.
                    # if(self._major[current][target+1] == "Yes"):
                    # Generate all permutations of chord with inversion (index)
                    for index_part in permutations(chord_list[0][pitch][i][0][1:]):
                        index = chord_list[0][pitch][i][0][0]+","+",".join(index_part)
                        if index not in self._map:
                            self._map[index] = {}
                        # Generate all permutations of chord with inversion (target)
                        for target_part in permutations(roman[0][1:]):
                            target_index = roman[0][0]+","+",".join(target_part)
                            if target_index not in self._map[index]:
                                self._map[index][target_index] = []
                            self._map[index][target_index].append([pitch, "Major", self._major_index[current], roman[1], self._majweight[current][target+1]])

        # Make minor chord flow
        for pitch in MusicManager.all_pitch_class:
            for i in range(0,len(chord_list[1][pitch])):
                current = self._minor_index.index(chord_list[1][pitch][i][1])   # current index no.
                for roman in chord_list[1][pitch]:
                    target = self._minor_index.index(roman[1])                  # target index no.
                    # if(self._minor[current][target+1] == "Yes"):
                    # Generate all permutations of chord with inversion (index)
                    for index_part in permutations(chord_list[1][pitch][i][0][1:]):
                        index = chord_list[1][pitch][i][0][0]+","+",".join(index_part)
                        if index not in self._map:
                            self._map[index] = {}
                        # Generate all permutations of chord with inversion (target)
                        for target_part in permutations(roman[0][1:]):
                            target_index = roman[0][0]+","+",".join(target_part)
                            if target_index not in self._map[index]:
                                self._map[index][target_index] = []
                            self._map[index][target_index].append([pitch, "Minor", self._minor_index[current], roman[1], self._minweight[current][target+1]])

        # for key in self._map:
        #     print("Map: ", key, self._map[key])


    def compare_chords(self, current, next):
        # compare two key and output the possible flow
        if current in self._map:
            if next in self._map[current]:
                logger.debug("OUTPUT: {} {} {}".format(current, next, self._map[current][next]))
                return self._map[current][next]

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


    def get_modulations(self, event_analyzer):
        """This function return the modulations of the given event_analyzer by comparing flows between chord """
        output_list = []
        event_groups = event_analyzer.event_container.event_groups
        number_of_measures = len(event_groups)
        # print(number_of_measures)
        for measure_number in range(number_of_measures):
            # compare the last event in previous measure and the first event in present measure
            if measure_number > 0 and len(event_groups[measure_number-1].events) > 0:
                #compare the events between measures
                before = event_groups[measure_number-1].events[-1]
                after = event_groups[measure_number].events[0]
                list_of_possible_keys = self.get_chord_flow_results(before, after)
                if list_of_possible_keys is not None:
                    output_list.append([before.event_group.measure, before.offset, list_of_possible_keys])

            for event_number in range(len(event_groups[measure_number].events)-1):
                # compare the events within a measure
                before = event_groups[measure_number].events[event_number]
                after = event_groups[measure_number].events[event_number+1]
                list_of_possible_keys = self.get_chord_flow_results(before, after)
                if list_of_possible_keys is not None:
                    output_list.append([before.event_group.measure, before.offset, list_of_possible_keys])

        # Obtain the most possible key using two chord flow
        output_key_list = []
        for i in range(1, len(output_list)):
            dict = {}
            current_flow = output_list[i][2]
            current_filtered_flow = []
            for flow in output_list[i-1][2]:
                dict[flow[0]+'-'+flow[1]] = flow[4]
            for flow in current_flow:
                if flow[0]+'-'+flow[1] in dict:
                    current_filtered_flow.append(flow)
            if current_filtered_flow == []:
                most_feasible_key = max(current_flow, key=lambda  t:t[4])
            else:
                most_feasible_key = max(current_filtered_flow, key=lambda  t:t[4]+dict[t[0]+'-'+t[1]])
            quality = True if most_feasible_key[1] == 'Major' else False
            a = [output_list[i][0], output_list[i][1], most_feasible_key[0], most_feasible_key[2], most_feasible_key[3], quality]
            output_key_list.append(a)

        # Copy the second flow result to first flow result
        if output_key_list == []:
            return
        second_element = output_key_list[0]
        # print("Append: ",output_list[0][0], output_list[0][1], output_list[0][2])
        for element in output_list[0][2]:
            if element[0] == second_element[2] and (element[1] == 'Major') == second_element[5]:
                output_key_list.insert(0, [output_list[0][0], output_list[0][1], element[0], element[2], element[3], element[1]=='Major'])
                break


        logger.debug("Select modulations with the highest weight")
        for key in output_key_list:
            quality = "Major" if key[5] else "Minor"
            logger.debug("Measure: {}\tOffset: {} {} {} {} {}".format(key[0], key[1], key[2], quality, key[3], key[4]))
        return output_key_list

    @staticmethod
    def unequal_matched_chord_event(current_event, next_event):
        if current_event.matched_chord == [] or next_event.matched_chord == []:
            return False
        if len(current_event.matched_chord) != len(next_event.matched_chord):
            return True
        else:
            i = 0
            for current_chord in current_event.matched_chord:
                for next_chord in next_event.matched_chord:
                    if set(current_chord) == set(next_chord):
                        i = i + 1
            if i == len(current_event.matched_chord):
                return False
            else:
                return True

    def compare_chords_oo(self, current, next):
        # compare two key and output the possible flow
        if current in self._map:
            if next in self._map[current]:
                logger.debug("OUTPUT: {} {} {}".format(current, next, self._map[current][next]))
                result_dict = { flow[0]+','+flow[1] : [flow[4], flow[2],flow[3]] for flow in self._map[current][next]}
                return result_dict

    def compare_event_oo(self, current,next):
        current_chord_key = ",".join(self.eliminate_inversion(current.matched_chord[0]))
        next_chord_key = ",".join(self.eliminate_inversion(next.matched_chord[0]))
        return self.compare_chords_oo(current_chord_key, next_chord_key)

    @staticmethod
    def get_common_key_by_statistic(event_list, filter={}):
        """ obtain the common key by statistic of the event_list
            input : [ measure, offset, chord_index, {'Key':[Weight, Roman1, Roman2] } ] ...
            output: { 'Key': Weight ... }
        """

        key_dict = {key : 0 for key in event_list[0][3]}

        for event in event_list:
            print("Correct: ",event[0], event[1], event[3])
            new_dict = {}
            for key in set(key_dict.keys()) & set(event[3].keys()):
                new_dict[key] = key_dict[key] + event[3][key][0]
            key_dict = new_dict
            print(key_dict)
        if key_dict != {}:
            if len(event_list) > 1 and key_dict[max(key_dict.keys(), key=lambda t: key_dict[t])] < 0:
                return {}
        return key_dict

    def get_modulations_oo(self, event_container):
        """This function return the modulations of the given event_analyzer by comparing flows between chord """
        output_list = []
        events = event_container.events
        before = events[0]
        for after in events:
            if after.matched_chord != []:
                before = after
                break
        if before.matched_chord == []:
            # Skip if all chord is unmatched
            return

        for after in events[1:]:
            if after.matched_chord != [] and self.unequal_matched_chord_event(before, after):
                list_of_possible_keys = self.compare_event_oo(before, after)
                output_list.append([before.event_group.measure, before.offset, before.chord, list_of_possible_keys])
                before = after

        # output list structure: [ measure, offset, chord_index, {'Key':[Weight, Roman1, Roman2] } ] ...

        for event in output_list:
            print("EVENT: ", event[0], event[1])
            for key in event[3]:
                print(" KEY: ", key, event[3][key])

        # Find the First NEXT CHORD using only max key and flow
        max_key = ""
        modulation = []
        next_chord = []
        weight = -100

        for event in output_list:
            if max_key not in event[3]:
                new_key_table = {}
                start = output_list.index(event)
                for length in range(0, 3):
                    if new_key_table == {}:
                        end = start + 4 - length
                        if end >= len(output_list):
                            new_key_table = self.get_common_key_by_statistic(output_list[start:])
                        else:
                            new_key_table = self.get_common_key_by_statistic(output_list[start:end])

                if new_key_table != {}:
                    max_key = max(new_key_table.keys(), key=lambda t: new_key_table[t])
                    weight = event[3][max_key][0]
                    modulation.append([event[0], event[1], event[2], max_key,
                                       event[3][max_key][1], event[3][max_key][2]])
            else:
                weight = weight + event[3][max_key][0]
                modulation.append([event[0], event[1], event[2], max_key,
                                   event[3][max_key][1], event[3][max_key][2]])
                if weight < 0:
                    max_key = ''
            print("TEST:",event[0], event[1], max_key, weight, event[2])

        for modulate in modulation:
            print(modulate)

if __name__ == "__main__":
    s = FlowState()
    # s.print_map()
    print(s.compare_chords("D,F#,A","G#,B,D"))
    print(s.match_chord_partial(['D', 'F', 'A']))
    print(s.match_chord_subset(['D','G#','A','B','C']))

    print(s.find_seven_chord(['A', 'C#','E']))
    print(s.remove_seven_chord(['B', 'D', 'G#', 'E']))
    print(s.match_chord_partial(['A', 'D', 'C']))
    print(s.eliminate_inversion(['A','C#','E']))
    print(s.match_chord_exact(['A','C#','E','G']))



