def detint(note1, note2, form):
    def nameint(diff):
        if diff == 1:
            interval = "minor second"
        elif diff == 2:
            interval = "major second"
        elif diff == 3:
            interval = "minor third"
        elif diff == 4:
            interval = "major third"
        elif diff == 5:
            interval = "perfect fourth"
        elif diff == 6:
            interval = "augmented fourth/diminished fifth"
        elif diff == 7:
            interval = "perfect fifth"
        elif diff == 8:
            interval = "minor sixth"
        elif diff == 9:
            interval = "major sixth"
        elif diff == 10:
            interval = "minor seventh"
        elif diff == 11:
            interval = "major seventh"
        elif diff == 0:
            interval = "perfect octave"
        else:
            pass
        return interval
    if type(note1) is int:
        notes = [int(note1), int(note2)]
        notes.sort()
        rdiff = notes[1]-notes[0]
        diff = rdiff%notes[0]
        if rdiff == 0:
            interval = "perfect unison"
        if form == "number of semitones":
            if rdiff == 0:
                print("interval is 0 semitones")
            else:
                print ("interval is {!s}".format(diff))
        elif form == "interval name":
            if rdiff == 0:
                print("interval is a perfect unison")
            else:
                nameint(diff)
                print("interval is a {!s}".format(interval))
    else:
        def conv(letter):
            if letter[0] == "C":
                value = 1
            elif letter[0] == "D":
                value = 3
            elif letter[0] == "E":
                value = 5
            elif letter[0] == "F":
                value = 6
            elif letter[0] == "G":
                value = 8
            elif letter[0] == "A":
                value = 10
            elif letter[0] == "B":
                value = 12
            else:
                print ("no note given")
            if len(letter)==2:
                if letter[1] == "+":
                    value += 1
                elif letter[1] == "-":
                    value -= 1
            else:
                pass
            return value
        num1 = conv(note1[0:2])
        num2 = conv(note2[0:2])
        if int(note1[-1]) == int(note2[-1]):
            if num1 == num2:
                val = 0
            elif num2 > num1:
                diff = (num2 - num1)
                val = 1
            else:
                diff = (num1-num2)
                val = 1
        else:
            if num1 < num2:
                diff = (num2-num1)
                val = 1
            else:
                diff = 12 - (num1-num2)
                val = 1
        if form == "number of semitones":
            if note1[1] == note2[1]:
                if interval == 0:
                    print("interval is 0 semitones")
            else:
                print ("interval is {!s}".format(interval))
        elif form == "interval name":
            if val == 0:
                print ("interval is a perfect unison")
            else:
                interval = nameint(diff)
                print ("interval is a {!s}".format(interval))

detint("A+4", "G-5", "interval name")
