import sys
import pickle

def save_obj(obj, name):
    with open('Scores/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def parseVector(filename, isTrain):
    res = []
    isTrain = False if isTrain not in ['1', 'True', 'true'] else True
    if isTrain == False:
        f = open(filename, "r")
        for line in f:
            line = line.rstrip()
            s = line.split(" | ")
            vector = []
            for i in s[1][1:-1].split(", "):
                vector.append(int(i))
            res.append(vector)
        f.close()
        return res
    
    validChord = None
    lchord = None
    testf = open(filename, "r")
    for line in testf:
        line = line.rstrip()
        s = line.split(" | ")
        ck = s[2].split(",")
        if len(ck) == 2:
            chord = ck[0]
            if chord != "N/A":
                validChord = chord
                break
                
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            s = line.split(" | ")
            measure, beat = s[0][1:-1].split(", ")
            vector = []
            for i in s[1][1:-1].split(", "):
                vector.append(int(i))
            ck = s[2].split(",")
            if len(ck)==2:
                chord, key = ck[0], ck[1]
                if chord == "N/A" and lchord is not None:
                    chord = lchord
                elif chord == "N/A" and lchord is None:
                    chord = validChord
                lchord, lkey = chord, ck[1]
            else:
                chord, key = lchord, lkey
            #res.append({"measure": measure, "beat":beat, "vector":vector, "chord":chord, "key":key})
            res.append((vector, chord))
    f.close()
    return res

if __name__ == "__main__":
    filename = sys.argv[1]
    isTrain = sys.argv[2]
    save_obj(parseVector(filename, isTrain), filename[:-4])