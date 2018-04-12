import os

from pyexcel import save_as
from pianoreduction.recognition.eventanalysis.lib import MusicManager
from pianoreduction import config

all_pitch_class = ["C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#",
                       "B"]

data_path = os.path.join(config.DATA_DIR, "recognition_model")

def n_trans(list, numOftrans):

        #split to n
        output_list = []
        for i in range(0, len(list)):
            if i < numOftrans-1:
                output_list.append([list[i]])
            else:
                temp = []
                for j in reversed(range(0, numOftrans)):
                    temp.append(list[i-j])
                output_list.append(temp)

        return output_list

def save_list(out, output_list):
        # create absolute path
        output_path = os.path.join(data_path, out)

        save_as(array=output_list, dest_file_name=output_path, dest_delimiter=',')

def create_map(Base_map ,pitch, major=True):
    # create mapping between the chord of key base and key pitch e.g C I -> G IV by comparing chord note
    current_map = MusicManager.get_instance().make_table(pitch, major)
    current_dict = {Base_roman[1]: current_roman[1] for Base_roman in Base_map
                    for current_roman in current_map
                    if Base_roman[0] == current_roman[0]}
    return current_dict


def ext_other_key(list, major=True):
    # create c major chord map as base map
    Base_map = MusicManager.get_instance().make_table("C", major)
    # print(Base_map)
    result_map = {}

    # create map with other key chord change equal c chord change
    for pitch in all_pitch_class:
        current_dict = create_map(Base_map, pitch)
        if len(current_dict)!= 0:
            result_map[pitch] = current_dict

        current_dict = create_map(Base_map, pitch, False)
        if len(current_dict) != 0:
            result_map[pitch+' min'] = current_dict

    for pitch in result_map:
        print(pitch, result_map[pitch])

    # label the input with Yes
    if major== True:
        output_list = [ row+[row[0]+"-"+row[1],"Yes" , "Major"] for row in list if len(row) != 1]
    else:
        output_list = [ row+[row[0]+"-"+row[1],"Yes", "Minor"] for row in list if len(row) != 1]

    # use the result map to extend result and label it with No
    for line in list:
        for pitch in result_map:
            result = [result_map[pitch][chord] if chord in result_map[pitch] else "N/A" for chord in line]
            if not all(x == "N/A" for x in result) and len(result) > 1:
                if 'min' in pitch:
                    output_list.append(result + [result[0]+"-"+result[1],"No", "Minor"])
                else:
                    output_list.append(result + [result[0]+"-"+result[1],"No", "Major"])

    # print result for reference
    for line in output_list:
        if 'N/A' not in line:
            print(line)

    return output_list







