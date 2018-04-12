# ------------------------
# This file has been deprecated but it is kept for reference purpose.
# All functionalities of this file are transferred and better organized in reduction.py
# ------------------------
import music21
import piano

xml_path = '../xml_scores/'
#xml_path = os.getcwd() + '/xml/result-correct/'
#xml_path = os.getcwd() + '/xml/'

#targetXml = 'full_1_18.xml'
targetXml = 'SQ-Original-fixed.xml'
#targetXml = 'full_34_48.xml'
#targetXml = 'full_136_150.xml'

#expectedXml = 'sample1_1_18.xml'
#expectedXml = 'sample1_34_48.xml'
#expectedXml = 'sample1_136_150.xml'

sampleInXml = [ 'SQ-Original-fixed.xml']
#sampleInXml = [ 'full_1_18.xml' ]
#sampleInXml = [ 'full_34_48.xml' ]
#sampleInXml = [ 'full_136_150.xml' ]
#sampleInXml = [ 'full_34_48.xml', 'full_136_150.xml' ]
#sampleInXml = [ 'full_1_18.xml', 'full_136_150.xml' ]
#sampleInXml = [ 'full_1_18.xml', 'full_34_48.xml' ]
#sampleInXml = [ 'full_1_18.xml', 'full_34_48.xml', 'full_136_150.xml' ]

sampleOutXml = [ 'SQ-Important entrances plus bass line 1.xml' ]
#sampleOutXml = [ 'SQ-Reducing by removing dissonances 1.xml' ]

#sampleOutXml = [ 'A_1_18.xml' ]
#sampleOutXml = [ 'A_34_48.xml' ]
#sampleOutXml = [ 'A_136_150.xml' ]
#sampleOutXml = [ 'A_34_48.xml', 'A_136_150.xml' ]
#sampleOutXml = [ 'A_1_18.xml', 'A_136_150.xml' ]
#sampleOutXml = [ 'A_1_18.xml', 'A_34_48.xml' ]
#sampleOutXml = [ 'A_1_18.xml', 'A_34_48.xml', 'A_136_150.xml' ]

#sampleOutXml = [ 'B_1_18.xml' ]
#sampleOutXml = [ 'B_34_48.xml' ]
#sampleOutXml = [ 'B_136_150.xml' ]
#sampleOutXml = [ 'B_34_48.xml', 'B_136_150.xml' ]
#sampleOutXml = [ 'B_1_18.xml', 'B_136_150.xml' ]
#sampleOutXml = [ 'B_1_18.xml', 'B_34_48.xml' ]
#sampleOutXml = [ 'B_1_18.xml', 'B_34_48.xml', 'B_136_150.xml' ]

# ------------------------------------------------------------------------------
print('read music score from file')

# target score
converter = music21.converter.subConverters.ConverterMusicXML()
converter.parseFile(xml_path+targetXml)
target = piano.score.Score(converter.stream)

# sample input
sampleIn = []
for sample in sampleInXml:
    converter = music21.converter.subConverters.ConverterMusicXML()
    converter.parseFile(xml_path+sample)
    sampleIn.append(piano.score.Score(converter.stream))
sampleOut = []
for sample in sampleOutXml:
    converter = music21.converter.subConverters.ConverterMusicXML()
    converter.parseFile(xml_path+sample)
    sampleOut.append(piano.score.Score(converter.stream))


# ------------------------------------------------------------------------------
print('building model')

# Guessing (include everything)
reducer = piano.reducer.Reducer(target)
reducer.addReductionAlgorithm(piano.algorithm.OnsetAfterRest())
#reducer.addReductionAlgorithm(piano.algorithm.StrongBeats(division=1))
reducer.addReductionAlgorithm(piano.algorithm.StrongBeats(division=0.5))
#reducer.addReductionAlgorithm(piano.algorithm.StrongBeats(division=0.25))
reducer.addReductionAlgorithm(piano.algorithm.ActiveRhythm())
reducer.addReductionAlgorithm(piano.algorithm.SustainedRhythm())
reducer.addReductionAlgorithm(piano.algorithm.RhythmVariety())
reducer.addReductionAlgorithm(piano.algorithm.VerticalDoubling())
reducer.addReductionAlgorithm(piano.algorithm.Occurrence())
reducer.addReductionAlgorithm(piano.algorithm.PitchClassStatistics(before=0, after=0))
reducer.addReductionAlgorithm(piano.algorithm.BassLine())
reducer.addReductionAlgorithm(piano.algorithm.EntranceEffect())


# ------------------------------------------------------------------------------
print('initialize training network and example')

for x in range(0, len(sampleIn)):
    reducer.addTrainingExample(sampleIn[x], sampleOut[x])
reducer.initAlgorithmKeys()
reducer.createAllMarkings()
reducer.createAlignmentMarkings()

dataset = None
for x in range(0, len(sampleIn)):
    dataset = sampleIn[x].TrainingDataSet(reducer=reducer, dataset=dataset)

# single layer
#network = piano.learning.buildNetwork(len(reducer.allKeys), 0, 1, bias=True, seed=0)

# multi layer
network = piano.learning.buildNetwork(len(reducer.allKeys), len(reducer.allKeys) * 2, 1, bias=True, seed=0)

trainer = piano.learning.BackpropTrainer(network, dataset, verbose=True)
print(reducer.allKeys)
# ------------------------------------------------------------------------------
print('show result')
result = music21.stream.Score()

trainer.trainUntilConvergence(maxEpochs = 300)
#trainer.trainUntilConvergence()
target.classify(network=network, reducer=reducer)
final_result = target.generatePianoScore(reduced=True, playable=True)

final_result.show('musicxml')
# GEX = music21.musicxml.m21ToXml.GeneralObjectExporter(final_result)
# out = GEX.parse()
# outStr = out.decode('utf-8')
# with open("testxml.xml", "w+") as xml:
#     print(outStr.strip(), file=xml)