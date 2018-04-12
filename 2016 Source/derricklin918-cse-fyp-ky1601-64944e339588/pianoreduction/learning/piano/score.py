import music21
import numpy

import pianoreduction.learning.piano.note as note
import pianoreduction.learning.piano.learning as learning


class Score(object):

    @property
    def score(self):
        return self._score

    @property
    def reducer(self):
        return self._reducer

    def __init__(self, score):

        self._score = music21.stream.Score()
        self._reducer = []

        _score = []
        _measureOffset = dict()
        _signature = dict()
        numOfMeasures = 0

        for part in score.parts:
            _part = dict()
            _score.append(_part)
            mid = 0

            measureOffset = 0
            measureLength = 0
            for measure in part.getElementsByClass(music21.stream.Measure):
                _measureOffset[mid] = measureOffset
                _measureOffset[mid+1] = measureOffset

                if measure.timeSignature is not None:
                    measureLength = measure.timeSignature.beatCount * measure.timeSignature.beatDuration.quarterLength

                #self.__addSignature(_signature, mid, measure.clef)
                self.__addSignature(_signature, mid, measure.timeSignature)
                self.__addSignature(_signature, mid, measure.keySignature)
                for elem in measure.offsetMap():
                    element = elem[0] #element
                    if isinstance(element, music21.note.GeneralNote) and not element.duration.isGrace:
                        self.__insertNote(_part, elem[3], mid, element, elem[1], elem[2] - elem[1])

                mid = mid + 1
                measureOffset = measureOffset + measureLength

            numOfMeasures = max(numOfMeasures, mid)

        for part in _score:
            for voice in part:
                for mid in _signature:
                    for key in _signature[mid]:
                        sign = _signature[mid][key]
                        part[voice][mid][min(part[voice][mid])].append((sign, 0))
        self.__postProcessInput(_score, numOfMeasures, _measureOffset)

    # END: def __init__(self, score)
    # --------------------------------------------------------------------------

    def __addSignature(self, signature, measure, sign):
        if sign is not None:
            if measure not in signature:
                signature[measure] = dict()
            signature[measure][type(sign)] = sign

    # END: def __addSignature(self, signature, measure, sign)
    # --------------------------------------------------------------------------

    def __insertNote(self, part=None, voice=None, measure=0, noteObj=None, offset=0, duration=1):
        if part is None or noteObj is None:
            return
        if voice is None:
            voice = 0

        if voice not in part:
            part[voice] = dict()
        if measure not in part[voice]:
            part[voice][measure] = dict()
        if offset not in part[voice][measure]:
            part[voice][measure][offset] = []
        part[voice][measure][offset].append((noteObj, duration))

    # END: def __insertNote(self, part, voice, measure, noteObj, offset, duration)
    # --------------------------------------------------------------------------

    def __postProcessInput(self, score, numOfMeasures, measureOffset):
        for part in score:
            _part = music21.stream.Part()
            self._score.insert(0, _part)

            tied = set()

            for vid in sorted(part):
                _voice = music21.stream.Voice()
                _part.insert(0, _voice)

                voice = part[vid]
                tiedNotes = dict()

                expect_mid = 0
                for mid in sorted(voice):
                    if (mid > expect_mid):
                        for i in range(expect_mid, mid):
                            _measure = music21.stream.Measure()
                            _measure.number = i
                            _measure.insert(0, music21.note.Rest(quarterLength=measureOffset[i+1]-measureOffset[i]))

                            _voice.append(_measure)

                    _measure = music21.stream.Measure()
                    _measure.number = mid
                    _voice.append(_measure)

                    measure = voice[mid]

                    delta_offset = sorted(measure)[0]
                    previous_endTime = 0
                    for offset in sorted(measure):
                        tuned_offset = offset - delta_offset

                        if (tuned_offset - previous_endTime) > 1e-5:
                            _measure.insert(previous_endTime, music21.note.Rest(quarterLength=(tuned_offset-previous_endTime)))

                        rests = False
                        notes = []
                        duration = 1024

                        for (noteObj, length) in measure[offset]:
                            if not isinstance(noteObj, music21.note.GeneralNote):
                                _measure.insert(offset, noteObj)
                                continue
                            if isinstance(noteObj, music21.note.NotRest):
                                if isinstance(noteObj, music21.chord.Chord):
                                    for ch_note in noteObj:
                                        tie = None
                                        if ch_note.tie is not None:
                                            tie = self.__postProcessWithTie(tied, ch_note)
                                        notes.append((ch_note.nameWithOctave, tie))
                                else:
                                    tie = None
                                    if noteObj.tie is not None:
                                        tie = self.__postProcessWithTie(tied, noteObj)
                                    notes.append((noteObj.nameWithOctave, tie))
                            duration = min(duration, length)

                        #if mid + 1 < len(measureOffset):
                            #duration = min(duration, measureOffset[mid+1] - measureOffset[mid] - tuned_offset)

                        insert_note = None
                        if len(notes) > 0:
                            if len(notes) > 1:
                                ch_notes = []
                                for noteObj in notes:
                                    ch_notes.append(self.__createNoteWithTuple(tiedNotes = tiedNotes, noteTuple = noteObj, quarterLength = duration))
                                insert_note = note.Chord(music21.chord.Chord(ch_notes))
                                insert_note.duration = music21.duration.Duration(duration)
                            else:
                                insert_note = self.__createNoteWithTuple(tiedNotes = tiedNotes, noteTuple = notes[0], quarterLength = duration)
                        else:
                            insert_note = note.Rest(music21.note.Rest(quarterLength=duration))

                        if duration > 1e-3:
                            _measure.insert(tuned_offset, insert_note)
                            previous_endTime = tuned_offset + duration

                    if previous_endTime < measureOffset[mid+1] - measureOffset[mid]:
                        _measure.insert(previous_endTime, note.Rest(music21.note.Rest(quarterLength=measureOffset[mid+1] - measureOffset[mid] - previous_endTime)))
                    expect_mid = mid + 1

                if expect_mid <= numOfMeasures:
                    for i in range(expect_mid, numOfMeasures):
                        _measure = music21.stream.Measure()
                        _measure.number = i
                        _measure.insert(0, music21.note.Rest())

                        _voice.append(_measure)

    # END: def __postProcessInput(self, score, numOfMeasures, measureOffset)
    # --------------------------------------------------------------------------

    def __createNoteWithTuple(self, tiedNotes = None, noteTuple = ('C4', None), quarterLength = 1):
        pitch = noteTuple[0]
        tied = noteTuple[1]

        noteObj = note.Note(music21.note.Note(pitch, quarterLength=quarterLength))
        if tied is not None:
            if tied == 'continue' or tied == 'stop':
                if pitch in tiedNotes and tiedNotes[pitch] is not None:
                    noteObj.tie_previous = tiedNotes[pitch]
                if tied == 'stop':
                    tiedNotes[pitch] = None

            if tied == 'start' or tied == 'continue':
                tiedNotes[pitch] = noteObj

            noteObj.tie = music21.tie.Tie(tied)
        return noteObj

    # END: def __createNotewithTuple(self, tiedNotes, noteTuple, quarterLength)
    # --------------------------------------------------------------------------

    def __postProcessWithTie(self, tied, noteObj):
        pitch = noteObj.nameWithOctave
        tieType = noteObj.tie.type
        if tieType == 'start':
            tied.add(pitch)
            return 'start'
        elif tieType == 'continue':
            return 'continue'
        elif tieType == 'stop':
            tied.remove(pitch)
            return 'stop'

    # END: def __postProcessWithTie(self, tied, noteObj)
    # --------------------------------------------------------------------------


    # not used
    def directMerge(self, parts=[]):
        result = music21.stream.Part()
        for pid in parts:
            part = self._score[pid]
            for voice in part.voices:
                result.insert(0, voice)
        return result

    # END: def directMerge(self, parts)
    # --------------------------------------------------------------------------


    # not used
    def merge(self, parts=[], reduced=True, measures=None):
        result = music21.stream.Part()
        for pid in parts:
            part = self._score[pid]
            partPs = []

            for voice in part.voices:
                retVoice = music21.stream.Voice()

                mid = 0
                for measure in voice.getElementsByClass(music21.stream.Measure):
                    retMeasure = music21.stream.Measure()
                    notes = []
                    lastNote = None

                    retMeasure.timeSignature = measure.timeSignature
                    retMeasure.keySignature = measure.keySignature

                    for noteObj in measure.notesAndRests:
                        if isinstance(noteObj, note.Rest):
                            if isinstance(lastNote, note.Rest):
                                lastNote.duration = music21.duration.Duration(lastNote.quarterLength + noteObj.quarterLength)
                            else:
                                lastNote = note.Rest(music21.note.Rest(duration=music21.duration.Duration(noteObj.quarterLength)))
                                lastNote.duration = music21.duraiton.Duration(noteObj.quarterLength)
                                notes.append(lastNote)
                        else:
                            if isinstance(noteObj, note.Chord):
                                chords = []
                                for ch_note in noteObj:
                                    if ch_note.align >= 0.5 or not reduced:
                                        chords.append(ch_note.nameWithOctave)
                                if len(chords) == 0:
                                    if isinstance(lastNote, note.Rest):
                                        lastNote.duration = music21.duration.Duration(lastNote.quarterLength + noteObj.quarterLength)
                                    else:
                                        lastNote = note.Rest(music21.note.Rest(duration=music21.duration.Duration(noteObj.quarterLength)))
                                        lastNote.duration = music21.duraiton.Duration(noteObj.quarterLength)
                                        notes.append(lastNote)
                                else:
                                    if len(chords) == 1:
                                        lastNote = note.Note(music21.note.Note(chords[0], duration=music21.duration.Duration(noteObj.quarterLength)))
                                        lastNote.duration = music21.duraiton.Duration(noteObj.quarterLength)
                                        notes.append(lastNote)
                                    else:
                                        lastNote = note.Chord(music21.chord.Chord(chords, duration=music21.duration.Duration(noteObj.quarterLength)))
                                        lastNote.duration = music21.duraiton.Duration(noteObj.quarterLength)
                                        notes.append(lastNote)
                            else:
                                if isinstance(noteObj, note.Note) and (noteObj.align >= 0.5 or not reduced):
                                    lastNote = note.Note(music21.note.Note(noteObj.nameWithOctave, duration=music21.duration.Duration(noteObj.quarterLength)))
                                    lastNote.duration = music21.duraiton.Duration(noteObj.quarterLength)
                                    lastNote.tie = noteObj.tie
                                    notes.append(lastNote)
                                else:
                                    if isinstance(lastNote, note.GeneralNote):
                                        lastNote.duration = music21.duration.Duration(lastNote.quarterLength + noteObj.quarterLength)
                                    else:
                                        lastNote = note.Rest(music21.note.Rest(duration=music21.duration.Duration(noteObj.quarterLength)))
                                        lastNote.duration = music21.duraiton.Duration(noteObj.quarterLength)
                                        notes.append(lastNote)
                    for nt in notes:
                        retMeasure.append(nt)
                        if isinstance(nt, note.Chord):
                            for noteObj in nt:
                                partPs.append(noteObj.ps)
                        elif isinstance(nt, note.Note):
                            partPs.append(nt.ps)

                    if measures is None or mid in measures:
                        retVoice.append(retMeasure)
                    mid = mid + 1

                result.insert(0, retVoice)

            median = numpy.median(partPs)

            clef = music21.clef.TrebleClef()
            if median < 60:
                clef = music21.clef.BassClef()

            for voice in result.voices:
                voice.measure(1).clef = clef
        return result

    # END: def merge(self, parts, reduced)
    # --------------------------------------------------------------------------

    def generatePianoScore(self, parts=[], reduced=True, playable=True, measures=None):

        leftRest = []
        leftHand = []

        rightRest = []
        rightHand = []

        measureLength = []
        measureOffset = []
        signature = []

        parts = (parts and [parts] or [range(0, len(self.score))])[0]

        for pid in parts:
            part = self.score[pid]

            for voice in part.voices:
                mid = 0
                for measure in voice.getElementsByClass(music21.stream.Measure):

                    while len(leftRest) < mid + 1:
                        leftRest.append([])
                    while len(leftHand) < mid + 1:
                        leftHand.append([])

                    while len(rightRest) < mid + 1:
                        rightRest.append([])
                    while len(rightHand) < mid + 1:
                        rightHand.append([])

                    while len(measureLength) < mid + 1:
                        measureLength.append(0)
                    while len(measureOffset) < mid + 1:
                        measureOffset.append(0)
                    measureOffset[mid] = measure.offset

                    while len(signature) < mid + 1:
                        signature.append((None, None))
                    signature[mid] = (measure.keySignature, measure.timeSignature)

                    restList = []
                    noteList = []
                    notePs = []

                    for noteObj in measure.notesAndRests:
                        measureLength[mid] = max(measureLength[mid], noteObj.offset + noteObj.quarterLength)

                        if isinstance(noteObj, note.Rest):
                            restList.append((noteObj.offset, noteObj.offset + noteObj.quarterLength))
                        elif isinstance(noteObj, note.Chord):
                            for ch_note in noteObj:
                                if ch_note.align >= 0.5 or not reduced:
                                    notePs.append(ch_note.pitch.ps)
                                    noteList.append((noteObj.offset, ch_note.nameWithOctave, ch_note.tie))
                        elif isinstance(noteObj, note.Note):
                            if noteObj.align >= 0.5 or not reduced:
                                notePs.append(noteObj.pitch.ps)
                                noteList.append((noteObj.offset, noteObj.nameWithOctave, noteObj.tie))

                    if len(noteList) > 0:
                        median = numpy.median(notePs)

                        if median < 60:
                            leftRest[mid].append(restList)
                            leftHand[mid].extend(noteList)
                        else:
                            rightRest[mid].append(restList)
                            rightHand[mid].extend(noteList)

                    mid = mid + 1

        leftStaff = music21.stream.Part()
        rightStaff = music21.stream.Part()

        leftTie = dict()
        rightTie = dict()

        for mid in range(0, len(leftHand)):
            if measures is None or mid in measures:
                rightMeasure = self.__createMeasure(notes=rightHand[mid], rests=rightRest[mid], tieRef=rightTie, measureLength=measureLength[mid], playable=playable, mid=None)
                leftMeasure = self.__createMeasure(notes=leftHand[mid], rests=leftRest[mid], tieRef=leftTie, measureLength=measureLength[mid], playable=playable, mid=None)

                if mid == 0:
                    rightMeasure.clef = music21.clef.TrebleClef()
                    leftMeasure.clef = music21.clef.BassClef()

                rightMeasure.keySignature = signature[mid][0]
                rightMeasure.timeSignature = signature[mid][1]

                leftMeasure.keySignature = signature[mid][0]
                leftMeasure.timeSignature = signature[mid][1]

                leftStaff.insert(measureOffset[mid], leftMeasure)
                rightStaff.insert(measureOffset[mid], rightMeasure)

        result = music21.stream.Score()

        result.insert(0, rightStaff)
        result.insert(0, leftStaff)

        staffGroup = music21.layout.StaffGroup([rightStaff, leftStaff], name='Marimba', abbreviation='Mba.', symbol='brace')
        staffGroup.barTogether = 'yes'

        result.insert(0, staffGroup)

        return result

    def __createMeasure(self, notes=[], rests=[], tieRef=dict(), measureLength=0, playable=True, mid=None):
        result = music21.stream.Measure()

        _notes = dict()
        for noteTuple in notes:
            if noteTuple[0] not in _notes:
                _notes[noteTuple[0]] = []
            _notes[noteTuple[0]].append((noteTuple[1], noteTuple[2]))

        _rests = dict()
        for restList in rests:
            for restTuple in restList:
                if restTuple[0] not in _rests:
                    _rests[restTuple[0]] = 0
                _rests[restTuple[0]] = _rests[restTuple[0]] + 1
                if restTuple[1] not in _rests:
                    _rests[restTuple[1]] = 0
                _rests[restTuple[1]] = _rests[restTuple[1]] - 1

        realNotes = []
        restCount = 0
        restStart = -1

        for offset in _rests:
            restCount = restCount + _rests[offset]
            if restStart == -1 and restCount == len(rests):
                restStart = offset
            elif restStart != -1 and restCount != len(rests):
                realNotes.append([restStart, 0, []])
                restStart = -1

        for offset in _notes:
            realNotes.append([offset, 0, _notes[offset]])

        realNotes = sorted(realNotes)

        if len(realNotes) > 0:
            first_note = realNotes[0]
            if len(first_note[2]) == 0:
                first_note[1] = first_note[1] + first_note[0]
                first_note[0] = 0
            elif abs(first_note[0]) > 1e-4:
                realNotes.append([0, first_note[0], []])

        realNotes = sorted(realNotes)

        if len(realNotes) > 1:
            for nid in range(0, len(realNotes) - 1):
                realNotes[nid][1] = realNotes[nid+1][0] - realNotes[nid][0]
            realNotes[len(realNotes) - 1][1] = measureLength - (realNotes[len(realNotes) - 1][0])

        ps = []
        for noteTuple in sorted(realNotes):
            _notes = noteTuple[2]

            if len(_notes) > 0:
                for _pitch in _notes:
                    if _pitch[1] is None or _pitch[1].type == 'start':
                        ps.append(music21.note.Note(_pitch[0]).pitch.ps)

        median = 60
        if len(ps) > 0:
            median = numpy.median(ps)
        # print median, ps

        if mid == 4:
            print(sorted(realNotes))
            print(realNotes)

        for noteTuple in sorted(realNotes):
            offset = noteTuple[0]
            duration = noteTuple[1]
            _notes = noteTuple[2]

            pitch = set()
            if len(_notes) > 0:
                for _pitch in _notes:
                    if _pitch[1] is None or _pitch[1].type == 'start':
                        pitch.add(_pitch[0])

            pitch = list(pitch)
            insertNote = None

            if len(pitch) > 1:

                ch_notes = []

                ch_max_ps = 0
                ch_max_note = None
                ch_min_ps = 1024
                ch_min_note = None

                for p in pitch:
                    noteObj = music21.note.Note(p, duration=music21.duration.Duration(duration))
                    ch_notes.append(noteObj)
                    if noteObj.pitch.ps > ch_max_ps:
                        ch_max_ps = noteObj.pitch.ps
                        ch_max_note = noteObj
                    if noteObj.pitch.ps < ch_min_ps:
                        ch_min_ps = noteObj.pitch.ps
                        ch_min_note = noteObj

                if playable:

                    while ch_max_ps - ch_min_ps > 12:
                        if median > 60:
                            ch_min_note.octave = ch_min_note.pitch.implicitOctave + 1
                        else:
                            ch_max_note.octave = ch_max_note.pitch.implicitOctave - 1

                        ch_max_ps = 0
                        ch_max_note = None
                        ch_min_ps = 1024
                        ch_min_note = None
                        for noteObj in ch_notes:
                            if noteObj.pitch.ps > ch_max_ps:
                                ch_max_ps = noteObj.pitch.ps
                                ch_max_note = noteObj
                            if noteObj.pitch.ps < ch_min_ps:
                                ch_min_ps = noteObj.pitch.ps
                                ch_min_note = noteObj

                insertNote = music21.chord.Chord(ch_notes)
                insertNote.duration = music21.duration.Duration(duration)
            elif len(pitch) == 1:
                insertNote = music21.note.Note(pitch[0], duration=music21.duration.Duration(duration))
            else:
                insertNote = music21.note.Rest(duration=music21.duration.Duration(duration))

            if mid == 4:
                print(insertNote, offset, duration, insertNote.quarterLength)
            if duration > 1e-2:
                result.insert(offset, insertNote)

        if not result.notesAndRests:
            result.insert(0, music21.note.Rest(duration=music21.duration.Duration(measureLength)))

        if mid == 4:
            result.show('text')

        return result

    # END: def generatePianoScore(self, parts, reduced)
    # --------------------------------------------------------------------------


    def TrainingDataSet(self, reducer=None, dataset=None):
        if reducer is None:
            return None

        #allKeys = sorted([ algo.key for algo in reducer.algorithms ])
        allKeys = reducer.allKeys
        inputCount = len(allKeys)

        if dataset is None:
            dataset = learning.SupervisedDataSet(inputCount, 1)

        for part in self.score:
            for voice in part.voices:
                for measure in voice.getElementsByClass(music21.stream.Measure):
                    for noteObj in measure.notes:
                        noteObj.addToDataSet(dataset=dataset, allKeys=allKeys)
        return dataset

    def classify(self, reducer=None, network=None):

        #allKeys = sorted([ algo.key for algo in reducer.algorithms ])
        allKeys = reducer.allKeys

        if network is None:
            return
        for part in self.score:
            for voice in part.voices:
                for measure in voice.getElementsByClass(music21.stream.Measure):
                    for noteObj in measure.notes:
                        noteObj.classify(network, allKeys)

    def threshold(self, reducer=None, threshold=0):

        #allKeys = sorted([ algo.key for algo in reducer.algorithms ])
        allKeys = reducer.allKeys

        for part in self.score:
            for voice in part.voices:
                for measure in voice.getElementsByClass(music21.stream.Measure):
                    for noteObj in measure.notes:
                        noteObj.threshold(threshold=threshold, allKeys=allKeys)

    def printClassifyResult(self):
        for part in self.score:
            for voice in part.voices:
                for measure in voice.getElementsByClass(music21.stream.Measure):
                    for noteObj in measure.notes:
                        if isinstance(noteObj, note.Chord):
                            for ch_note in noteObj:
                                print(ch_note, ch_note.align)
                        else:
                            print(noteObj, noteObj.align)
