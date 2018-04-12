import numpy
import random

from pybrain.structure.networks import FeedForwardNetwork
# from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import LinearLayer, TanhLayer, SigmoidLayer, BiasUnit, FullConnection
from pybrain.structure.modules.neuronlayer import NeuronLayer
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader

from scipy import tanh

class ZeroOneLayer(NeuronLayer):
    def _forwardImplementation(self, inbuf, outbuf):
        func = lambda x: (x >= 0.95 and [1] or (x <= 0.05 and [0] or [x]))[0]
        outbuf[:] = map(func, tanh(inbuf))

    def _backwardImplementation(self, outerr, inerr, outbuf, inbuf):
        inerr[:] = (1 - outbuf**2) * outerr

def buildNetwork(InputLength=1, HiddenLength=0, OutputLength=1, bias=True, seed=None):

    network = FeedForwardNetwork()
    input_layer = LinearLayer(InputLength)
    if HiddenLength > 0:
        hidden_layer = SigmoidLayer(HiddenLength)
    output_layer = SigmoidLayer(OutputLength)

    network.addInputModule(input_layer)
    network.addOutputModule(output_layer)
    if HiddenLength > 0:
        network.addModule(hidden_layer)

    if HiddenLength > 0:
        network.addConnection(FullConnection(input_layer, hidden_layer))
        network.addConnection(FullConnection(hidden_layer, output_layer))
    else:
        network.addConnection(FullConnection(input_layer, output_layer))

    if bias:
        bias_node = BiasUnit()
        network.addModule(bias_node)
        network.addConnection(FullConnection(bias_node, input_layer))
        if HiddenLength > 0:
            network.addConnection(FullConnection(bias_node, hidden_layer))
        network.addConnection(FullConnection(bias_node, output_layer))

    network.sortModules()

    numpy.random.seed(seed)
    random.seed(seed)
    network.randomize()
    
    #print network.params

    return network
