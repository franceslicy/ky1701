import pianoreduction.learning.piano.algorithm as algorithm

class Reducer(object):
    def __init__(self, score):
        super(Reducer, self).__init__()
        self._score = score
        self._examples = []
        self._algorithms = []

    @property
    def allKeys(self):
        return sorted([ key for algo in self.algorithms for key in algo.allKeys ])

    @property
    def algorithms(self):
        return self._algorithms

    # END: def __init(self, fullScore)
    # --------------------------------------------------------------------------

    def addTrainingExample(self, sampleInput, sampleOutput):
        self._examples.append((sampleInput, sampleOutput))

    # END: def addTrainingData(self, sampleInput, sampleOutput)
    # --------------------------------------------------------------------------

    def addReductionAlgorithm(self, algorithm):
        self._algorithms.append(algorithm)

    # END: def addReductionAlgorithm(self, algorithm)
    # --------------------------------------------------------------------------

    def initAlgorithmKeys(self):
        num = 0
        for algo in self._algorithms:
            algo.key = num
            num = num + 1

    # END: def initAlgorithmKeys(self)
    # --------------------------------------------------------------------------

    def createAllMarkings(self):
        #print tuple([ algo.key for algo in self._algorithms])
        for algo in self._algorithms:
            algo.createMarkingsOn(self._score)

            for example in self._examples:
                algo.createMarkingsOn(example[0])

    # END: def createAllMarkings(self)
    # --------------------------------------------------------------------------

    def createAlignmentMarkings(self):
        align = algorithm.SimpleAlignment()
        for example in self._examples:
            align.alignScores(example[0], example[1])
