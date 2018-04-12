import os

from pyexcel_xlsx import save_data

from pianoreduction.recognition.eventanalysis.lib import MusicManager
from pianoreduction import config

data_path = os.path.join(config.DATA_DIR, "recognition_model")

class ModelConverter:

    def __init__(self):
        # Prepare index
        self._major_index = MusicManager.major_progression_extend_index
        self._minor_index = MusicManager.minor_progression_extend_index

        # Prepare path
        self._major_model_path = os.path.join(data_path, "majorwekamodel.txt")
        self._major_input_path = os.path.join(data_path, "Chord Flow - Major keys.xlsx")
        self._major_output_path = os.path.join(data_path, "major_flow_weight.xlsx") # TODO: change to .csv format
        self._major_display_path = os.path.join(data_path, "major_flow_weight_normalized.xlsx")

        self._minor_model_path = os.path.join(data_path, "minorwekamodel.txt")
        self._minor_input_path = os.path.join(data_path, "Chord Flow - Minor keys.xlsx")
        self._minor_output_path = os.path.join(data_path, "minor_flow_weight.xlsx") # TODO: change to .csv format
        self._minor_display_path = os.path.join(data_path, "minor_flow_weight_normalized.xlsx")

        # Open File
        self._major_file = open(self._major_model_path, "r")
        self._minor_file = open(self._minor_model_path, "r")

        # Major parse model
        self._major_weight = self.ParseFile(self._major_file, self._major_index)
        self.save_weight(self._major_output_path, self._major_weight)
        self._major_display = self.create_percentage_map(self._major_weight)
        self.save_weight(self._major_display_path, self._major_display)

        # Minor parse model
        self._minor_weight = self.ParseFile(self._minor_file, self._minor_index)
        self.save_weight(self._minor_output_path, self._minor_weight)
        self._minor_display = self.create_percentage_map(self._minor_weight)
        self.save_weight(self._minor_display_path, self._minor_display)


    def ParseFile(self, file, index):
        # Prepare weight map
        weight = [[y] + [0.0 for x in index] for y in index]
        norm = 0

        # Parse Each line
        for line in file:
            words = line.split()
            match = words[-1].split("=")
            if match[0] == '1':
                # Row Weight
                print(match[1])
                current_index = index.index(match[1])
                for num in range(0, len(index)):
                    weight[current_index][num+1] += float(words[1])

            elif match[0] == '2':
                # Column Weight
                current_index = index.index(match[1])
                for num in range(0, len(index)):
                    weight[num][current_index+1] += float(words[1])

            elif match[0] == 'Trans':
                # Cell Weight
                cell_chords = match[1].split('-')
                current_index = index.index(cell_chords[0])
                next_index = index.index(cell_chords[1])
                weight[current_index][next_index+1] += float(words[1])

        # add index
        weight = [['(Major Key) From:']+ index] + weight
        return weight

    def Print_weight(self):
        for line in self._major_weight:
            print("Major", line)
        for line in self._minor_weight:
            print("Minor", line)

    def save_weight(self, link, data):
        sheetx = {
            "Sheet1" : data
        }
        save_data(link, sheetx)

    def mean_value(self, value, max, min):
        maximum = max - min
        normalized_value = value - min
        return round(100 * normalized_value / maximum, 3)



    def create_percentage_map(self, data):
        min = data[1][1]
        max = data[1][1]
        for row in data:
            for cell in row:
                if type(cell) is float:
                    max =  cell if cell > max else max
                    min =  cell if cell < min else min

        percentage_map = [[self.mean_value(cell, max, min) if type(cell) is float else cell
                                        for cell in row]
                                        for row in data]
        return percentage_map



s = ModelConverter()
s.Print_weight()
