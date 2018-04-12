import os
import ChordIdentifier
import music21
import sys
import time

# This is a driving program of the ChordIdentifier module

# read input file path
curPath = os.getcwd() + '/'
try:
	inputFilename = sys.argv[1]
except IndexError:
	print "Fail to read input file name" 
	sys.exit(1)

# read input
print "Reading input musicxml file"
try:
	rawScore = music21.converter.parse(curPath+inputFilename)  #for relative path
except music21.converter.ConverterException:
	try:
		rawScore = music21.converter.parse(inputFilename)  #for absolute path
	except music21.converter.ConverterException:
		print "Fail to read input file"
		sys.exit(1)
inputFilename = inputFilename.split('/')[-1]

# generate or load saved Identifier Object
identifier = ChordIdentifier.Identifier.getIdentifier(score=rawScore, scoreFilename=inputFilename)

# print debug message of loaded Music Score
# identifier.printPreparedScore()

verifierFeatureClass = ChordIdentifier.ProgressionVerifier.ProgressionFeature
verifierIntervalChoiceClass = ChordIdentifier.ProgressionVerifier.ProgressionIntervalChoice

# for time calculation
startMs = round(time.time()*1000)

# all possible feature combination for OnBeat mode, comment the unwanted features
identifier.runProgression(choice=verifierIntervalChoiceClass.OnBeat, featureList=[verifierFeatureClass.ChordFunction], verbal=False, output=True)
identifier.runProgression(choice=verifierIntervalChoiceClass.OnBeat, featureList=[verifierFeatureClass.FirstComeFirstServe], verbal=False, output=True)
identifier.runProgression(choice=verifierIntervalChoiceClass.OnBeat, featureList=[verifierFeatureClass.VtoIProgression, verifierFeatureClass.ChordFunction], verbal=False, output=True)
identifier.runProgression(choice=verifierIntervalChoiceClass.OnBeat, featureList=[verifierFeatureClass.VtoIProgression, verifierFeatureClass.FirstComeFirstServe], verbal=False, output=True)


# all possible feature combination for AllIntervalType mode, comment the unwanted features
identifier.runProgression(choice=verifierIntervalChoiceClass.AllIntervalType, featureList=[verifierFeatureClass.ChordFunction], verbal=False, output=True)
identifier.runProgression(choice=verifierIntervalChoiceClass.AllIntervalType, featureList=[verifierFeatureClass.FirstComeFirstServe], verbal=False, output=True)
identifier.runProgression(choice=verifierIntervalChoiceClass.AllIntervalType, featureList=[verifierFeatureClass.VtoIProgression, verifierFeatureClass.ChordFunction], verbal=False, output=True)
identifier.runProgression(choice=verifierIntervalChoiceClass.AllIntervalType, featureList=[verifierFeatureClass.VtoIProgression, verifierFeatureClass.FirstComeFirstServe], verbal=False, output=True)


# all possible feature combination for ChangedBaseline mode, comment the unwanted features
identifier.runProgression(choice=verifierIntervalChoiceClass.ChangedBaseline, featureList=[verifierFeatureClass.ChordFunction], verbal=False, output=True)
identifier.runProgression(choice=verifierIntervalChoiceClass.ChangedBaseline, featureList=[verifierFeatureClass.FirstComeFirstServe], verbal=False, output=True)
identifier.runProgression(choice=verifierIntervalChoiceClass.ChangedBaseline, featureList=[verifierFeatureClass.VtoIProgression, verifierFeatureClass.ChordFunction], verbal=False, output=True)
identifier.runProgression(choice=verifierIntervalChoiceClass.ChangedBaseline, featureList=[verifierFeatureClass.VtoIProgression, verifierFeatureClass.FirstComeFirstServe], verbal=False, output=True)

finishMs = round(time.time()*1000)

totalMs = int(finishMs - startMs)
print "Time used: "+str(int(round(totalMs/1000)))+"s "+str(totalMs%1000)+"ms"