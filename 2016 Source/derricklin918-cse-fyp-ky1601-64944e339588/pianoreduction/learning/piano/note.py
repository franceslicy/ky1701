import copy

import music21
import pianoreduction.learning.piano.base as base

# multiple inheritance is used here because there is no better solution
# to let music21 recognize my data and adding more attributes together
class GeneralNote(base.PianoReductionObject, music21.note.GeneralNote):
    def __init__(self, ref):
        super(GeneralNote, self).__init__(ref)
        self._marks = dict()
        self._align = 0

    def addMark(self, key, value):
        self._marks[key] = value

    @property
    def marks(self):
        return self._marks

    # if the note is aligned or not, { 0, 1 }
    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, align):
        self._align = align

    # to generate input data based on all labels provided
    def dataInput(self, allKeys=[]):
        ret = tuple([ ((key in self._marks) and [self._marks[key]] or [0])[0] for key in allKeys ])
        return ret

    @property
    def dataOutput(self):
        return (float(self.align))

    def addToDataSet(self, dataset=None, allKeys=[]):
        if dataset is None:
            return
        dataset.addSample(self.dataInput(allKeys), self.dataOutput)

    # classify a note based on a given network
    def classify(self, network=None, allKeys=[]):
        if network is None:
            self.align = 0
            return
        self.align = network.activate(self.dataInput(allKeys))[0]

    # classify a note based on linear combination and a threshold
    def threshold(self, allKeys=[], threshold=0):
            self.align = ((sum(self.dataInput(allKeys)) >= threshold) and [1] or [0])[0]

# END: class GeneralNote(base.PianoReductionObject, music21.note.GeneralNote)
# ------------------------------------------------------------------------------

class Rest(GeneralNote, music21.note.Rest):
    def __init__(self, ref):
        if isinstance(ref, music21.note.NotRest):
            rest = music21.note.Rest()
            rest.duration = ref.duration
            rest.quarterLength = ref.quarterLength
            rest.offset = ref.offset
            super(Rest, self).__init__(rest)
        else:
            super(Rest, self).__init__(ref)

class NotRest(GeneralNote, music21.note.NotRest):
    def __init__(self, ref):
        super(NotRest, self).__init__(ref)
        self.tie_previous = None

    @property
    def align(self):
        if self.tie_previous is not None:
            return self.tie_previous.align
        return self._align

    @align.setter
    def align(self, align):
        if self.tie_previous is None:
            self._align = align

class Note(NotRest, music21.note.Note):
    def __init__(self, ref):
        super(Note, self).__init__(ref)

class Chord(NotRest, music21.chord.Chord):
    def __init__(self, ref):
        super(Chord, self).__init__(ref)

    def addMark(self, key, value):
        for noteObj in self:
            noteObj._marks[key] = value

    def addToDataSet(self, dataset=None, allKeys=[]):
        for noteObj in self:
            noteObj.addToDataSet(dataset=dataset, allKeys=allKeys)

    def classify(self, network=None, allKeys=[]):
        if network is None:
            return
        for noteObj in self:
            noteObj.align = network.activate(noteObj.dataInput(allKeys))[0]

    def threshold(self, allKeys=[], threshold=0):
        for noteObj in self:
            noteObj.align = ((sum(noteObj.dataInput(allKeys)) >= threshold) and [1] or [0])[0]
