import numpy as np
from hmm_class import hmm
import pickle

CHORD_LIST = ['I', 'I+', 'IIb', 'II', 'II7', 'III', 'IV', 'V', 'V7', 'V+', 'V+7', 'VIb', 'VI','VI7','VIGer', 'VII', 'VII7', 'VIIGer', 'VIIIta', 'VIIdim', 'VIIdim7']

CHORD_IN_VEC = {
    'I': [1, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0],
    'I+': [1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0],
    'IIb': [0, 1, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0],
    'II': [0, 0, 1, 0, 0, 2, 0, 0, 0, 3, 0, 0],
    'II7': [4, 0, 1, 0, 0, 2, 0, 0, 0, 3, 0, 0],
    'III': [0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 3],
    'IV': [3, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0],
    'V': [0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 2],
    'V7': [0, 0, 3, 0, 0, 4, 0, 1, 0, 0, 0, 2],
    'V+': [0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 2],
    'V+7': [0, 0, 0, 3, 0, 4, 0, 1, 0, 0, 0, 2],
    'VIb': [2, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0],
    'VI': [2, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0],
    'VI7': [2, 0, 0, 0, 3, 0, 0, 4, 0, 1, 0, 0],
    'VIGer': [0, 2, 0, 0, 3, 0, 4, 0, 0, 1, 0, 0],
    'VII': [0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 0, 1],
    'VII7': [0, 0, 2, 0, 0, 3, 0, 0, 0, 4, 0, 1],
    'VIIGer': [0, 0, 0, 2, 0, 0, 3, 0, 4, 0, 0, 1],
    'VIIIta': [0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 1],
    'VIIdim': [0, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
    'VIIdim7': [0, 2, 0, 0, 3, 0, 0, 4, 0, 0, 0, 1]
}

def load_obj(name):
    with open('Scores/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def vec2dec(hmmvector):
    res = 0
    for i in range(len(hmmvector)):
        res += hmmvector[i] * (2 ** (11-i))
    return res

def dec2vec(num):
    res_string = '{0:012b}'.format(num)
    res = []
    for i in res_string:
        res.append(int(i))
    return res

def deg_sim(vector, chord):
    chord_vec = CHORD_IN_VEC[chord]
    deg = 0
    if 4 in chord_vec:
        for i in range(12):
            if vector[i] == 1 and chord_vec[i] == 0:
                deg += -1
            elif vector[i] == 1 and chord_vec[i] == 1:
                deg += 5
            elif vector[i] == 1 and chord_vec[i] == 2:
                deg += 3
            elif vector[i] == 1 and chord_vec[i] == 3:
                deg += 1
            elif vector[i] == 1 and chord_vec[i] == 4:
                deg += 1
    else:
        for i in range(12):
            if vector[i] == 1 and chord_vec[i] == 0:
                deg += -1
            elif vector[i] == 1 and chord_vec[i] == 1:
                deg += 5
            elif vector[i] == 1 and chord_vec[i] == 2:
                deg += 3
            elif vector[i] == 1 and chord_vec[i] == 3:
                deg += 2
    if deg < 0:
        deg = 0
    return deg
    

def load_train_files():
    train_file = open("Scores/train_file.txt","r")
    filelist = []
    for line in train_file:
        line = line.rstrip()
        filelist.append(line)
    train_file.close()
    
    data = []
    for f in filelist:
        data.append(load_obj(f))
        print("Train file " + f + " has been loaded")
    print("\n")
    return data

def load_test_files():
    test_file = open("Scores/test_file.txt","r")
    filelist = []
    for line in test_file:
        line = line.rstrip()
        filelist.append(line)
    test_file.close()
    
    data = []
    for f in filelist:
        data.append(load_obj(f))
        print("Test file " + f + " has been loaded")
    print("\n")
    return data, filelist

if __name__ == "__main__":
    states = CHORD_LIST
    possible_observation = tuple(range(4096))
    train_data = load_train_files()
    occurence_count = {}
    transition_dict = {}
    for chord in CHORD_LIST:
        occurence_count.update({chord: 0})
    for chord1 in CHORD_LIST:
        transition_dict.update({chord1: {}})
        for chord2 in CHORD_LIST:
            transition_dict[chord1].update({chord2: 0})
    total_count = 0
    for f in train_data:
        last_chord = None
        for tup in f:
            if last_chord is not None:
                transition_dict[last_chord][tup[1]] += 1
            last_chord = tup[1]
            occurence_count[tup[1]] += 1
            total_count += 1
    print("Total chord events recorded: " + str(total_count)+"\n")
    for chord1 in transition_dict:
        trans_count = 0
        for chord2 in transition_dict[chord1]:
            trans_count += transition_dict[chord1][chord2]
        for chord2 in transition_dict[chord2]:
            if trans_count != 0:
                transition_dict[chord1][chord2] /= trans_count
            else:
                transition_dict[chord1][chord1] = 1
    transition_prob = []
    for chord1 in transition_dict:
        tmp_list = []
        for chord2 in transition_dict[chord1]:
            tmp_list.append(transition_dict[chord1][chord2])
        if transition_prob == []:
            for i in tmp_list:
                transition_prob.append(i)
            transition_prob = np.array(transition_prob)
        else:
            transition_prob = np.vstack((transition_prob, tmp_list))
    transition_prob = np.asmatrix(transition_prob)
    
    for i in range(21):
        for j in range(21):
            transition_prob[i,j] = 1/21
    
    start_prob = []
    for key in occurence_count:
        start_prob.append(occurence_count[key]/total_count)
    start_prob = np.asmatrix(start_prob)
    emission_dict = {}
    for chord in CHORD_LIST:
        emission_dict.update({chord: []})
    for i in range(4096):
        for chord in emission_dict:
            deg = deg_sim(dec2vec(i), chord)
            if 4 in CHORD_IN_VEC[chord]:
                if deg == 0:
                    emission_dict[chord].append(0)
                elif deg == 1:
                    emission_dict[chord].append(1/55/440)
                elif deg == 2:
                    emission_dict[chord].append(2/55/418)
                elif deg == 3:
                    emission_dict[chord].append(3/55/375)
                elif deg == 4:
                    emission_dict[chord].append(4/55/340)
                elif deg == 5:
                    emission_dict[chord].append(5/55/298)
                elif deg == 6:
                    emission_dict[chord].append(6/55/220)
                elif deg == 7:
                    emission_dict[chord].append(7/55/121)
                elif deg == 8:
                    emission_dict[chord].append(8/55/45)
                elif deg == 9:
                    emission_dict[chord].append(9/55/10)
                elif deg == 10:
                    emission_dict[chord].append(10/55)
            else:
                if deg == 0:
                    emission_dict[chord].append(0)
                elif deg == 1:
                    emission_dict[chord].append(1/55/418)
                elif deg == 2:
                    emission_dict[chord].append(2/55/397)
                elif deg == 3:
                    emission_dict[chord].append(3/55/361)
                elif deg == 4:
                    emission_dict[chord].append(4/55/312)
                elif deg == 5:
                    emission_dict[chord].append(5/55/248)
                elif deg == 6:
                    emission_dict[chord].append(6/55/171)
                elif deg == 7:
                    emission_dict[chord].append(7/55/94)
                elif deg == 8:
                    emission_dict[chord].append(8/55/37)
                elif deg == 9:
                    emission_dict[chord].append(9/55/10)
                elif deg == 10:
                    emission_dict[chord].append(10/55)
    emission_prob = []
    for chord in emission_dict:
        if emission_prob == []:
            emission_prob = emission_dict[chord]
            emission_prob = np.array(emission_prob)
        else:
            emission_prob = np.vstack((emission_prob, emission_dict[chord]))
    emission_prob = np.asmatrix(emission_prob)
    
    diff = []
    for i in range(21):
        summation = 0
        for j in range(4096):
            summation += emission_prob[i,j]
        diff.append(1-summation)
    emission_prob[0,2192] += diff[0]
    emission_prob[1,2184] += diff[1]
    emission_prob[2,1096] += diff[2]
    emission_prob[3,580] += diff[3]
    emission_prob[4,2628] += diff[4]
    emission_prob[5,145] += diff[5]
    emission_prob[6,2116] += diff[6]
    emission_prob[7,529] += diff[7]
    emission_prob[8,593] += diff[8]
    emission_prob[9,273] += diff[9]
    emission_prob[10,337] += diff[10]
    emission_prob[11,2312] += diff[11]
    emission_prob[12,2180] += diff[12]
    emission_prob[13,2196] += diff[13]
    emission_prob[14,1188] += diff[14]
    emission_prob[15,577] += diff[15]
    emission_prob[16,581] += diff[16]
    emission_prob[17,297] += diff[17]
    emission_prob[18,265] += diff[18]
    emission_prob[19,1153] += diff[19]
    emission_prob[20,1169] += diff[20]
    
    observation_tuple = []
    for f in train_data:
        obs = []
        for tup in f:
            obs.append(vec2dec(tup[0]))
        obs = tuple(obs)
        observation_tuple.append(obs)
    quantities_observations = []
    for i in range(len(train_data)):
        quantities_observations.append(1)
    
    model = hmm(states, possible_observation, start_prob, transition_prob, emission_prob)
    
    test_data, name = load_test_files()
    for i in range(len(test_data)):
        dec_list = []
        for vec in test_data[i]:
            dec_list.append(vec2dec(vec))
        dec_tup = tuple(dec_list)
        print("Test result for " + name[i] + ": ")
        print(model.viterbi(dec_tup))
        print("\n")