import json
import logging
import os
import time
import music21
import pianoreduction.learning.piano.score as score
import pianoreduction.learning.piano.reducer as reducer
import pianoreduction.learning.piano.algorithm as algorithm
import pianoreduction.learning.piano.learning as learning

from pianoreduction import config
from pianoreduction.learning.postprocessor import PostProcessor

"""
.. module:: reduction
    :platform: Unix
    :synopsis: This module serves as main class for piano reduction.

.. moduleauthor:: Derrick Lin <derricklin918@gmail.com>, Wing Au <auho1234@gmail.com>

Example:
    Run this module standalone to generate a piano reduction result in MusicXML format opened in preferred notation software
        $ python reduction.py

Attributes:
    targetXml (str): The file name for piano reduction.
    sampleInXml ([str]): A list of files as training sample inputs.
    sampleOutXml ([str]): A list of files as training sample outputs.
    model_folder (str): the path where models are saved.
"""
# ===== logger setting =====
log_file_name = time.strftime("%Y%m%d-%H%M%S" + ".log")
log_file_path = os.path.join(config.LOG_DIR, log_file_name)
logger = logging.getLogger("Reduction")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(name)s %(levelname)s %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

file = logging.FileHandler(log_file_path, mode='w')
file.setLevel(logging.DEBUG)

logger.addHandler(file)
# ===== logger setting end =

targetXml = 'SQ-Original-fixed.xml'

sampleInXml = ['SQ-Original-fixed.xml']

sampleOutXml = ['SQ-Important entrances plus bass line 1.xml']

model_folder = config.MODELS_DIR

# ------------------------------------------------------------------------------


class PianoReduction:
    """
    Main class for piano reduction package. Use this class to create piano reductions.

    Attributes:
        target (learning.piano.score.Score): the target score under piano reduction.
        reducer (learning.piano.reducer.Reducer): Reducer class for managing reduction algorithms.
        sampleIn ([music21.score.Score]): score samples for training models.
        sampleOut ([music21.score.Score]): piano-reduced score samples for training models.
        reduced_score (music21.score.Score): piano-reduced score output by the neural network. Default value is a string.
        username (str): the name of user who starts the reduction.
        score_name (str): the name of the score.
    """
    def __init__(self, target_xml, username):
        """
        PianoReduction initializer.

        :param target_xml: the file name (with extension .xml) of target score.
        :param username: the name of user who starts the reduction.
        """
        logger.info("Initializing PianoReduction object.")
        logger.info("Username: {} Date: {}".format(username, time.strftime("%c")))
        converter = music21.converter.subConverters.ConverterMusicXML()
        logger.info("Parsing {}".format(target_xml))
        converter.parseFile(os.path.join(config.SCORE_DIR, target_xml))
        self._target = score.Score(converter.stream)
        self._reducer = reducer.Reducer(self._target)
        self._sampleIn = []
        self._sampleOut = []
        self._reduced_score = "No Reduction Score"
        self._username = username
        self._score_name = os.path.splitext(target_xml)[0]

    def add_sample_in(self, sample_in_xml):
        """
        Add sample scores as input for training

        :param sample_in_xml: the list of xml files (in file names) to be added
        :return: None
        """
        logger.info("Adding reduction input samples")
        for sample in sample_in_xml:
            logger.info(sample)
            # create music21 Score object from MusicXML
            converter = music21.converter.subConverters.ConverterMusicXML()
            converter.parseFile(os.path.join(config.SCORE_DIR, sample))
            self._sampleIn.append(score.Score(converter.stream))

    def add_sample_out(self, sample_out_xml):
        """
        Add reduced sample scores as output for training

        :param sample_out_xml: the list of xml files (in file names) to be added
        :return: None
        """
        logger.info("Adding reduction output samples")
        for sample in sample_out_xml:
            logger.info(sample)
            # create music21 Score object from MusicXML
            converter = music21.converter.subConverters.ConverterMusicXML()
            converter.parseFile(os.path.join(config.SCORE_DIR, sample))
            self._sampleOut.append(score.Score(converter.stream))

    def build_model(self, OnsetAfterRest=1, StrongBeats=1, StrongBeatsDivision=0.5, ActiveRhythm=1,
                    SustainedRhythm=1, RhythmVariety=1, VerticalDoubling=1, Occurrence=1, PitchClassStatistics=1,
                    PitchClassStatisticsBefore=0, PitchClassStatisticsAfter=0, BassLine=1, EntranceEffect=1, Dissonance=1):
        """
        Build the model based on reduction algorithm parameters.

        :param OnsetAfterRest: Mark all notes at the beginning of a bar or sound after any rests.
        :param StrongBeats: Mark all notes in strong beats.
        :param StrongBeatsDivision: As a parameter for strong beats. The unit of strong beats quarter notes = 0.25, half notes = 0.5, whole notes = 1
        :param ActiveRhythm: For multi-part music, an active rhythm is a part with most number of notes in one measure. Mark notes in active rhythms.
        :param SustainedRhythm: opposite of active rhythm. A part with least number of notes is in sustained rhythm. Mark notes in sustained rhythms.
        :param RhythmVariety: Mark notes that are responsible for changing rhythms.
        :param VerticalDoubling: Mark notes that they have the same pitch class but different octaves.
        :param Occurrence:  Mark notes of pitch classes with highest octaves for each voices and parts.
        :param PitchClassStatistics: Mark pitch classes with highest frequency for each measures.
        :param PitchClassStatisticsBefore:
        :param PitchClassStatisticsAfter:
        :param BassLine: Mark notes in bass lines.
        :param EntranceEffect: Mark notes after rest.
        :param Dissonance: Mark all dissonances.
        """
        logger.info('Adding reduction algorithm parameters')
        self._model = {}
        self._model = locals().copy()
        self._model.pop('self')

        logger.info("OnsetAfterRest : {}".format(OnsetAfterRest))
        logger.info("StrongBeats : {}".format(StrongBeats))
        logger.info("StrongBeatsDivision : {}".format(StrongBeatsDivision))
        logger.info("ActiveRhythm : {}".format(ActiveRhythm))
        logger.info("SustainedRhythm : {}".format(SustainedRhythm))
        logger.info("RhythmVariety : {}".format(RhythmVariety))
        logger.info("VerticalDoubling : {}".format(VerticalDoubling))
        logger.info("Occurrence : {}".format(Occurrence))
        logger.info("PitchClassStatistics : {}".format(PitchClassStatistics))
        logger.info("PitchClassStatisticsBefore : {}".format(PitchClassStatisticsBefore))
        logger.info("PitchClassStatisticsAfter : {}".format(PitchClassStatisticsAfter))
        logger.info("BassLine : {}".format(BassLine))
        logger.info("EntranceEffect : {}".format(EntranceEffect))
        logger.info("Dissonance : {}".format(Dissonance))
        # Default: Guessing (include everything)
        if(OnsetAfterRest == 1):
            self._reducer.addReductionAlgorithm(algorithm.OnsetAfterRest())
        if (StrongBeats == 1):
            self._reducer.addReductionAlgorithm(algorithm.StrongBeats(division=StrongBeatsDivision))
        if (ActiveRhythm == 1):
            self._reducer.addReductionAlgorithm(algorithm.ActiveRhythm())
        if (SustainedRhythm == 1):
            self._reducer.addReductionAlgorithm(algorithm.SustainedRhythm())
        if (RhythmVariety == 1):
            self._reducer.addReductionAlgorithm(algorithm.RhythmVariety())
        if (VerticalDoubling == 1):
            self._reducer.addReductionAlgorithm(algorithm.VerticalDoubling())
        if (Occurrence == 1):
            self._reducer.addReductionAlgorithm(algorithm.Occurrence())
        if (PitchClassStatistics == 1):
            self._reducer.addReductionAlgorithm(algorithm.PitchClassStatistics(before=PitchClassStatisticsBefore, after=PitchClassStatisticsAfter))
        if (BassLine == 1):
            self._reducer.addReductionAlgorithm(algorithm.BassLine())
        if (EntranceEffect == 1):
            self._reducer.addReductionAlgorithm(algorithm.EntranceEffect())
        if (Dissonance == 1):
            self._reducer.addReductionAlgorithm(algorithm.Dissonance())


    def init_training_samples(self):
        """
        initialize all training samples

        :return: None
        """
        logger.debug("Initialize training samples and reduction algorithms")
        for x in range(0, len(self._sampleIn)):
            self._reducer.addTrainingExample(self._sampleIn[x], self._sampleOut[x])
        self.init_reducer_algorithm()

    def init_reducer_algorithm(self):
        """
        initialize all reduction algorithms and create markings on all scores.
        :return: None
        """
        logger.debug("Create markings of the score with reduction algorithms.")
        self._reducer.initAlgorithmKeys()
        self._reducer.createAllMarkings()
        self._reducer.createAlignmentMarkings()

    def set_threshold(self, threshold):
        """
        Set the threshold for piano reduction to determine whether a note is kept in model
        :param threshold: integer to determine whether a note is kept
        :return: None
        """
        self._target.threshold(self._reducer, threshold)

    def train_network(self, maxEpochs=300, verbose=False):
        """
        Training neural network.
        :param maxEpochs: number of epochs of training.
        :param verbose: True for verbose debug output.
        :return: None
        """
        logger.info("Starting training network with epoch {}".format(maxEpochs))
        dataset = None
        for x in range(0, len(self._sampleIn)):
            dataset = self._sampleIn[x].TrainingDataSet(reducer=self._reducer, dataset=dataset)

        # single layer
        #self._network = learning.buildNetwork(len(self._reducer.allKeys), 0, 1, bias=True, seed=0)

        # multi layer (currently using)
        self._network = learning.buildNetwork(len(self._reducer.allKeys), len(self._reducer.allKeys) * 2, 1, bias=True, seed=0)

        trainer = learning.BackpropTrainer(self._network, dataset, verbose=True)
        logger.info(self._reducer.allKeys)

        trainer.trainUntilConvergence(maxEpochs=maxEpochs)
        # trainer.trainUntilConvergence()
        logger.info("Training completed")
        self._target.classify(network=self._network, reducer=self._reducer)

    def generate_reduced_score(self):
        """
        Generate reduced score to a music21.score.Score object.
        :return: None
        """
        logger.info("Generate reduced score with trained result")
        self._reduced_score = self._target.generatePianoScore(reduced=True, playable=True)
        logger.debug("Initialize post processor to add additional data and info to the generated score")
        self._post_processor = PostProcessor(self._target, self._reduced_score)
        logger.info("Adding username and score name to the score")
        self._post_processor.fill_meta_data(self._username, self._score_name)
        logger.info("Adding roman numeral notations")
        self._post_processor.embed_romans()
        self._post_processor.color_dissonance()

    def show_result(self):
        """
        Output reduction result to preferred notation software for viewing.
        :return: None
        """
        logger.debug("Showing the result to score viewer")
        if isinstance(self._reduced_score, music21.stream.Score):
            self._reduced_score.show("musicxml")
        else:
            logger.info("No reduced score")

    def get_xml(self):
        """
        Get the reduced score as MusicXML in string.
        :return: string in MusicXML format
        """
        GEX = music21.musicxml.m21ToXml.GeneralObjectExporter(self._reduced_score)
        out = GEX.parse()
        outStr = out.decode('utf-8')
        return outStr

    def save_network(self, filename):
        """
        Save the trained network as two files in model folder. The .xml file is neural network data generated by pybrain.
        The .json file is reduction algorithm parameter data.
        :param filename: the name of a trained model to be saved
        :return: None
        """
        learning.NetworkWriter.writeToFile(self._network, os.path.join(model_folder, filename + ".xml"))
        with open(os.path.join(model_folder, filename + ".json"), "w") as file:
            json.dump(self._model, file)
        file.close()

    def load_network(self, filename):
        """

        :param filename: the name of the trained model to be loaded
        :return: None
        """
        self._model = {}
        # load reduction algorithm parameters
        with open(os.path.join(model_folder, filename + ".json"), "r") as file:
            self._model = json.load(file)
        file.close()
        logger.info(self._model)
        # initialize reducer
        self._reducer = reducer.Reducer(self._target)
        # build the model based on reduction algorithms selected
        self.build_model(**self._model)
        # initialize algorithms and create markings on all sample scores
        self._reducer.initAlgorithmKeys()
        self._reducer.createAllMarkings()
        self._reducer.createAlignmentMarkings()
        # load network model
        self._network = learning.NetworkReader.readFrom(os.path.join(model_folder, filename + ".xml"))
        # generate reduction result by the network
        self._target.classify(network=self._network, reducer=self._reducer)

# three ways to generate piano reduction are written in methods
def learning_reduction(p, epoch = 300, features = {}):
    """
    Generate piano reduction by learning. This method first trains a neural network model with samples provided.
    When the network is trained, generate piano reduction result by applying the model and show the score in notation software.
    :param p: PianoReduction object.
    :param epoch: the number of epochs for training.
    :param features: reduction algorithm parameters in dictionary.
    :return: None
    """
    # add all samples for training
    p.add_sample_in(sampleInXml)
    p.add_sample_out(sampleOutXml)
    # build model based on reduction algorithm parameters
    p.build_model(**features)
    # initialize training samples
    p.init_training_samples()
    # start training
    p.train_network(maxEpochs=epoch, verbose=False)
    # generate reduced score from the model
    p.generate_reduced_score()
    # show the result to music notation software
    p.show_result()

def save_load_reduction(p, epoch=300, file_name="default", features={}):
    """
    Generate a reduction and save the trained network model if the file_name does not exist.
    If the file_name exists, generate a reduction by loading up a saved model.

    :param p: PianoReduction object.
    :param epoch: the number of epochs for training
    :param file_name: the name of a trained model to be saved/loaded
    :param features: reduction algorithm parameters in dictionary.
    :return:
    """
    # if the file_name exists, start loading.
    if os.path.exists(os.path.join(model_folder, file_name + ".xml")) and os.path.exists(os.path.join(model_folder, file_name + ".json")):
        logger.info("Neural network model \"{}\" found. Now loading model and output".format(file_name))
        p.load_network(file_name)
        p.generate_reduced_score()
        p.show_result()
    else:
        # start training a new model.
        logger.info("Neural network model \"{}\" not found. Now start learning".format(file_name))
        p.add_sample_in(sampleInXml)
        p.add_sample_out(sampleOutXml)
        p.build_model(**features)
        p.init_training_samples()
        p.train_network(maxEpochs=epoch, verbose=False)
        p.generate_reduced_score()
        p.show_result()
        # if no file_name is set, use time as the file name
        if file_name == "default":
            save_name = time.strftime("%Y%m%d-%H%M%S")
        else:
            save_name = file_name
        p.save_network(save_name)

def simple_reduction(p, features={}, threshold=5):
    """

    :param p: PianoReduction object
    :param features: the name of a trained model to be saved/loaded
    :param threshold: integer to determine whether a note is kept
    :return:
    """
    # build model based on reduction algorithm parameters
    p.build_model(**features)
    # initalize all reduction algorithms
    p.init_reducer_algorithm()
    # set the threhold
    p.set_threshold(threshold)
    # generate reduction score
    p.generate_reduced_score()
    # show the score in notation software
    p.show_result()


# for internal testing
if __name__ == "__main__":
    parameters = {'OnsetAfterRest' : 1,
                  'StrongBeats' : 1,
                  'StrongBeatsDivision' : 0.5,
                  'ActiveRhythm' : 1,
                  'SustainedRhythm' : 1,
                  'RhythmVariety' : 1,
                  'VerticalDoubling' : 1,
                  'Occurrence' : 1,
                  'PitchClassStatistics' : 1,
                  'PitchClassStatisticsBefore' : 0,
                  'PitchClassStatisticsAfter' : 0,
                  'BassLine' : 1,
                  'EntranceEffect' : 1,
                  'Dissonance' : 1
                  }
    p = PianoReduction(targetXml, "KY1601")
    # save_load_reduction(p, epoch = 5, file_name="test", features = parameters)
    learning_reduction(p, epoch = 10, features=parameters)
    # simple_reduction(p, features=parameters)