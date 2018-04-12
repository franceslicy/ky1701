import time
import logging
import os
from pianoreduction import config
from pianoreduction.learning.reduction import PianoReduction
from flask import Flask, request

"""
.. module:: api
    :platform: Unix
    :synopsis: This module setups HTTP APIs for piano reduction

.. moduleauthor:: Derrick Lin <derricklin918@gmail.com>

Attributes:
    app (Flask): flask app object.
    model_folder (String): it specifies the directory where the trained models are saved.
"""

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
# TODO: multiple-threading

model_folder = config.MODELS_DIR

@app.route("/")
def test():
    """
    This function serves as a test for connection to backend server.

    Returns:
        str: returns "Hello World" upon function completion.
    """
    return "Hello World"

@app.route("/learn", methods=['POST'])
def learn_reduction():
    """
    Learning parameters:
    OnsetAfterRest : Int [0 or 1]
    StrongBeats : Int [0 or 1]
    StrongBeatsDivision : Float [0.25 or 0.5 or 1]
    ActiveRhythm : Int [0 or 1]
    SustainedRhythm : Int[0 or 1]
    RhythmVariety : Int [0 or 1]
    VerticalDoubling : Int [0 or 1]
    Occurrence : Int [0 or 1]
    PitchClassStatistics : Int[0 or 1]
    PitchClassStatisticsBefore : (not decided yet, use 0 for now)
    PitchClassStatisticsAfter (not decided yet, use 0 for now)
    BassLine : Int [0 or 1]
    EntranceEffect : Int [0 or 1]
    Dissonance : Int [0 or 1]

    modelName(optional) : String
    targetXml : String
    sampleInXml : Array of strings of .xml files
    sampleOutXml : Array of strings of .xml files

    Example Form:
    OnsetAfterRest:1
    StrongBeats:1
    StrongBeatsDivision:0.5
    ActiveRhythm:1
    SustainedRhythm:1
    RhythmVariety:1
    VerticalDoubling:1
    Occurrence:1
    PitchClassStatistics:1
    PitchClassStatisticsBefore:0
    PitchClassStatisticsAfter:0
    BassLine:1
    EntranceEffect:1
    Dissonance:1
    modelName:test
    targetXml:SQ-Original-fixed.xml
    sampleInXml[]:SQ-Original-fixed.xml
    sampleOutXml[]:SQ-Important entrances plus bass line 1.xml

    Returns:
        str: when the model is successfully trained, return music xml in response.
    """
    # setting up parameters from HTTP request body
    parameters = {'OnsetAfterRest': int(request.form['OnsetAfterRest']),
                  'StrongBeats': int(request.form['StrongBeats']),
                  'StrongBeatsDivision': float(request.form['StrongBeatsDivision']),
                  'ActiveRhythm': int(request.form['ActiveRhythm']),
                  'SustainedRhythm': int(request.form['SustainedRhythm']),
                  'RhythmVariety': int(request.form['RhythmVariety']),
                  'VerticalDoubling': int(request.form['VerticalDoubling']),
                  'Occurrence': int(request.form['Occurrence']),
                  'PitchClassStatistics': int(request.form['PitchClassStatistics']),
                  'PitchClassStatisticsBefore': int(request.form['PitchClassStatisticsBefore']),
                  'PitchClassStatisticsAfter': int(request.form['PitchClassStatisticsAfter']),
                  'BassLine': int(request.form['BassLine']),
                  'EntranceEffect': int(request.form['EntranceEffect']),
                  'Dissonance': int(request.form['Dissonance'])
                  }
    # the name of the model going to be saved
    model_file = request.form['modelName']

    # if the model name is blank, use time as the name instead
    if model_file == "":
        model_file = time.strftime("%Y%m%d-%H%M%S")

    # if there exists reduction_models with the same name, stop and return
    if os.path.exists(os.path.join(model_folder, model_file + ".xml")) or os.path.exists(os.path.join(model_folder, model_file + ".json")):
        logging.info("Model file exists. Change into a unique name. Reduction process halted")
        return "Model file exists. Change into a unique name. Reduction process halted"
    # the target .xml file for piano reduction
    target_xml_file = request.form['targetXml']
    # a list of reduction sample (before reduction)
    sample_in_xml = request.form.getlist('sampleInXml[]')
    # a list of reduction sample (after reduction)
    sample_out_xml = request.form.getlist('sampleOutXml[]')

    logging.info("Name of target File: {}".format(target_xml_file))
    logging.info("Name of model: {}".format(model_file))
    logging.info("Sample In List: {}".format(sample_in_xml))
    logging.info("Sample Out List: {}".format(sample_out_xml))

    logging.info("Parameters:\n {}".format(parameters))

    # create piano reduction object
    # TODO: add username param to POST method
    p = PianoReduction(target_xml_file, "<username>")
    # add reduction samples
    p.add_sample_in(sample_in_xml)
    p.add_sample_out(sample_out_xml)
    # build neural network model from parameters
    p.build_model(**parameters)
    # initialize the network
    p.init_training_samples()
    # start training
    p.train_network(maxEpochs=5)
    p.generate_reduced_score()
    p.show_result()
    # save the network
    p.save_network(model_file)
    # return .xml content in response
    return p.get_xml()

@app.route("/load", methods=['POST'])
def load_reduction():
    """
    targetXml : String
    modelFile : String

    Example Form:
    targetXml:SQ-Original-fixed.xml
    modelFile:20170212-233326

    Returns:
        str: return music xml in response when the model is loaded successfully. Else return error string.
    """

    # retrieve necessary files
    target_xml_file = request.form['targetXml']
    model_file = request.form['modelFile']

    if os.path.exists(model_folder + model_file + ".xml") and os.path.exists(model_folder + model_file + ".json"):
        logging.info("Name of target file: {}".format(target_xml_file))
        logging.info("Name of model to be loaded: {}".format(model_file))
        # create piano reduction object
        p = PianoReduction(target_xml_file, "<username>")
        # load the network parameters
        p.load_network(model_file)
        p.generate_reduced_score()
        # show reduction result in preferred notation software
        p.show_result()
        # return .xml content in response
        return p.get_xml()

    else:
        logging.info("Failed to load the model: Necessary files not found")
        return "Failed to load the model: Necessary files not found"

@app.route("/simple", methods=['POST'])
def simple_reduction():
    """
        Learning parameters:
        OnsetAfterRest : Int [0 or 1]
        StrongBeats : Int [0 or 1]
        StrongBeatsDivision : Float [0.25 or 0.5 or 1]
        ActiveRhythm : Int [0 or 1]
        SustainedRhythm : Int[0 or 1]
        RhythmVariety : Int [0 or 1]
        VerticalDoubling : Int [0 or 1]
        Occurrence : Int [0 or 1]
        PitchClassStatistics : Int[0 or 1]
        PitchClassStatisticsBefore : (not decided yet, use 0 for now)
        PitchClassStatisticsAfter (not decided yet, use 0 for now)
        BassLine : Int [0 or 1]
        EntranceEffect : Int [0 or 1]
        Dissonance : Int [0 or 1]
        Threshold : Int

        modelName(optional) : String
        targetXml : String

        Example Form:
        OnsetAfterRest:1
        StrongBeats:1
        StrongBeatsDivision:0.5
        ActiveRhythm:1
        SustainedRhythm:1
        RhythmVariety:1
        VerticalDoubling:1
        Occurrence:1
        PitchClassStatistics:1
        PitchClassStatisticsBefore:0
        PitchClassStatisticsAfter:0
        BassLine:1
        EntranceEffect:1
        Dissonance:1
        Threshold:5
        modelName:test
        targetXml:SQ-Original-fixed.xml

        Returns:
            str: return music xml in response.
        """
    # the target .xml file for piano reduction
    parameters = {'OnsetAfterRest': int(request.form['OnsetAfterRest']),
                  'StrongBeats': int(request.form['StrongBeats']),
                  'StrongBeatsDivision': float(request.form['StrongBeatsDivision']),
                  'ActiveRhythm': int(request.form['ActiveRhythm']),
                  'SustainedRhythm': int(request.form['SustainedRhythm']),
                  'RhythmVariety': int(request.form['RhythmVariety']),
                  'VerticalDoubling': int(request.form['VerticalDoubling']),
                  'Occurrence': int(request.form['Occurrence']),
                  'PitchClassStatistics': int(request.form['PitchClassStatistics']),
                  'PitchClassStatisticsBefore': int(request.form['PitchClassStatisticsBefore']),
                  'PitchClassStatisticsAfter': int(request.form['PitchClassStatisticsAfter']),
                  'BassLine': int(request.form['BassLine']),
                  'EntranceEffect': int(request.form['EntranceEffect']),
                  'Dissonance': int(request.form['Dissonance'])
                  }
    threshold = int(request.form['Threshold'])
    target_xml_file = request.form['targetXml']

    # TODO: add username param to POST method
    p = PianoReduction(target_xml_file, "<username>")
    p.build_model(**parameters)
    p.init_reducer_algorithm()
    p.set_threshold(threshold)
    p.generate_reduced_score()
    # show reduction result in preferred notation software
    p.show_result()
    return p.get_xml()