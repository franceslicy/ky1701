import sys

def parseVector(filename):
    res = []
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
                lchord, lkey = ck[0], ck[1]
            else:
                chord, key = lchord, lkey
            res.append({"measure": measure, "beat":beat, "vector":vector, "chord":chord, "key":key})
    f.close()
    return res

filename = sys.argv[1]
print(parseVector(filename))