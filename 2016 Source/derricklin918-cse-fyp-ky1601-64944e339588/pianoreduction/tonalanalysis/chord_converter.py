# ------------------------
# This file has been deprecated but it is kept for reference purpose.
# All functionalities of this file are transferred to result_parser.py
# ------------------------
import os
from math import exp, log

from pyexcel_xlsx import get_data, save_data

from pianoreduction import config

data_path = os.path.join(config.DATA_DIR, "recognition_model")

class ChordConverter:

    @property
    def map(self):
        return self._major_map

    @property
    def sheet_major(self):
        return self._major_index

    @property
    def sheet_minor(self):
        return self._minor_index

    all_pitch_class = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#",
                       "B"]
    all_chord_type = ["Major", "Minor", "Dim", "Aug", "Sus4"]

    def __init__(self):
        # Create chordlist by chordtype and key for indexing
        # C Major C Minor C Dim ...
        self._chord = []
        for pitch in self.all_pitch_class:
            for chord in self.all_chord_type:
                self._chord.append(" ".join((pitch, chord)))
                
        # Prepare path
        self._major_model_path = os.path.join(data_path, "majortransmodel.txt")
        self._major_input_path = os.path.join(data_path, "Chord Flow - Major keys.xlsx")
        self._major_output_path = os.path.join(data_path, "MajorProp.xlsx")

        self._minor_model_path = os.path.join(data_path, "minortransmodel.txt")
        self._minor_input_path = os.path.join(data_path, "Chord Flow - Minor keys.xlsx")
        self._minor_output_path = os.path.join(data_path, "MinorProp.xlsx")


        # Major get model data
        self._major_file = open(self._major_model_path, "r")
        self._major_map = []
        for line in self._major_file:
            self._major_map.append(float(line))
        self._major_index = get_data(self._major_input_path, start_row=0)["Sheet2"]

        # Minor get model data
        self._minor_file = open(self._minor_model_path, "r")
        self._minor_map = []
        for line in self._minor_file:
            self._minor_map.append(float(line))
        self._minor_index = get_data(self._minor_input_path, start_row=0)["Sheet2"]



    def getmajorvalue(self, current, next):
        # obtain the model value of respective chord flow
        return self._major_map[current * 60 + next]

    def getminorvalue(self, current, next):
        # obtain the model value of respective chord flow
        return self._minor_map[current * 60 + next]



    def print_majorsheet(self):
        # Get data for index
        data = get_data(self._major_input_path)["Sheet1"]
        full_list = [data[0]]

        # Create result
        for row in self._major_index:
            list = [row[0]]
            for secrow in self._major_index:
                if row[1] is None or secrow[1] is None:
                    list.append(None)
                else:
                    current = self._chord.index(row[1])
                    next = self._chord.index(secrow[1])
                    if current == next:
                        list.append(-36)
                    else:
                        list.append(self.getmajorvalue(current, next))
            full_list.append(list)
        print(full_list)

        # Save result
        sheetx = {
            "Sheet1" : full_list
        }
        save_data(self._major_output_path, sheetx)

        # Calculate Correctness using the Chord Flow file
        data = get_data(self._major_input_path, start_row=1)["Sheet1"]
        Yessum = 0.0
        Yes = 0
        Nosum = 0.0
        No = 0
        data[len(self._major_index) - 1].append(None)
        for row in range(0, len(self._major_index)):
            for column in range(0, len(self._major_index)):
                if data[row][column+1] == "Yes":
                    Yes+= 1
                    Yessum += exp(full_list[row+1][column+1])
                else:
                    No+= 1
                    Nosum += exp(full_list[row+1][column+1])
        print("Yes: ", Yes, Yessum, Yessum/Yes, "No: ",No, Nosum, Nosum/No)
        self._majorsum = Yessum+Nosum
        self._majorcount = Yes+No

    def print_minorsheet(self):
        # Get data for index
        data = get_data(self._minor_input_path)["Sheet1"]
        full_list = [data[0]]

        # Create result
        for row in self._minor_index:
            list = [row[0]]
            for secrow in self._minor_index:
                if row[1] is None or secrow[1] is None:
                    list.append(None)
                else:
                    current = self._chord.index(row[1])
                    next = self._chord.index(secrow[1])
                    if current == next:
                        list.append(-36)
                    else:
                        list.append(self.getminorvalue(current, next))
            full_list.append(list)
        print(full_list)

        # Save result
        sheetx = {
            "Sheet1" : full_list
        }
        save_data(self._minor_output_path, sheetx)

        # Calculate Correctness using the Chord Flow file
        data = get_data(self._minor_input_path, start_row=1)["Sheet1"]
        Yessum = 0.0
        Yes = 0
        Nosum = 0.0
        No = 0
        data[len(self._minor_index) - 1].append(None)
        for row in range(0, len(self._minor_index)):
            for column in range(0, len(self._minor_index)):
                if data[row][column+1] == "Yes":
                    Yes+= 1
                    Yessum += exp(full_list[row+1][column+1])
                else:
                    No+= 1
                    Nosum += exp(full_list[row+1][column+1])
        print("Yes: ", Yes, Yessum, Yessum/Yes, "No: ",No, Nosum, Nosum/No)

        # Display the correctness of Major and Minor
        self._minorsum = Yessum + Nosum
        self._minorcount = Yes + No
        print(self._majorcount, self._majorsum, self._majorsum / self._majorcount, self._minorcount, self._minorsum,
              self._minorsum / self._minorcount)

    def standardizeMinor(self):
        # Standardize the error of Major and Minor to Major

        # Get data
        full_list = get_data(self._minor_output_path)["Sheet1"]

        # Normalize data
        normalize_value = self._majorsum/self._majorcount
        normalize_value *= self._minorcount/self._minorsum
        for row in full_list[1:]:
            for column in range(1, len(row)):
                    value = exp(row[column])*normalize_value
                    row[column] = log(value)

        # Store data
        sheetx = {
            "Sheet1": full_list
        }
        save_data(self._minor_output_path, sheetx)

        # Calculate Correctness using the Chord Flow file
        data = get_data(self._minor_input_path, start_row=1)["Sheet1"]
        Yessum = 0.0
        Yes = 0
        Nosum = 0.0
        No = 0
        data[len(self._minor_index) - 1].append(None)
        for row in range(0, len(self._minor_index)):
            for column in range(0, len(self._minor_index)):
                if data[row][column + 1] == "Yes":
                    Yes += 1
                    Yessum += exp(full_list[row + 1][column + 1])
                else:
                    No += 1
                    Nosum += exp(full_list[row + 1][column + 1])
        print("Yes: ", Yes, Yessum, Yessum / Yes, "No: ", No, Nosum, Nosum / No)


        # Display the correctness of Major and Minor
        self._minorsum = Yessum + Nosum
        self._minorcount = Yes + No
        print(self._majorcount, self._majorsum, self._majorsum/self._majorcount, self._minorcount, self._minorsum, self._minorsum/self._minorcount)







s = ChordConverter()
print("Major")
s.print_majorsheet()
print("Minor")
s.print_minorsheet()
s.standardizeMinor()