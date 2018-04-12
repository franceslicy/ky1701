import numpy as np
from music21 import *
from simplenn import *

# parse the target music xml file to a music21 Score data type
score = converter.parse('/Users/derricklin/Development/piano-reduction/chord-identification/scores/d-major-first.xml')
right_hand = score.parts[0]

first_measure = right_hand.getElementsByClass(stream.Measure)[0]
chord = first_measure.getElementsByClass(chord.Chord)[0]
print(chord.pitchClasses)

def pitchClassesToInput(pitchClasses):
    chordArray = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
    for x in pitchClasses:
        chordArray[x] = 1
    return chordArray

a = pitchClassesToInput(chord.pitchClasses)
print(a)

np.random.seed(5)

hidden_layer = NeuronLayer(12, 24)
output_layer = NeuronLayer(24, 1)

dumb_network = NeuralNetwork(hidden_layer, output_layer)

dumb_network.print_weights()

c_major = [1,0,0,0,1,0,0,1,0,0,0,0]
c_minor = [1,0,0,1,0,0,0,1,0,0,0,0]

db_major = [0,1,0,0,0,1,0,0,1,0,0,0]
cs_minor = [0,1,0,0,1,0,0,0,1,0,0,0]

d_major = [0,0,1,0,0,0,1,0,0,1,0,0]
d_minor = [0,0,1,0,0,1,0,0,0,1,0,0]

eb_major = [0,0,0,1,0,0,0,1,0,0,1,0]
ds_minor = [0,0,0,1,0,0,1,0,0,0,1,0]

e_major = [0,0,0,0,1,0,0,0,1,0,0,1]
e_minor = [0,0,0,0,1,0,0,1,0,0,0,1]

f_major = [1,0,0,0,0,1,0,0,0,1,0,0]
f_minor = [1,0,0,0,0,1,0,0,1,0,0,0]

fs_major = [0,1,0,0,0,0,1,0,0,0,1,0]
fs_minor = [0,1,0,0,0,0,1,0,0,1,0,0]

g_major = [0,0,1,0,0,0,0,1,0,0,0,1]
g_minor = [0,0,1,0,0,0,0,1,0,0,1,0]

ab_major = [1,0,0,1,0,0,0,0,1,0,0,0]
gs_minor = [0,0,0,1,0,0,0,0,1,0,0,1]

a_major = [0,1,0,0,1,0,0,0,0,1,0,0]
a_minor = [1,0,0,0,1,0,0,0,0,1,0,0]

bb_major = [0,0,1,0,0,1,0,0,0,0,1,0]
as_minor = [0,1,0,0,0,1,0,0,0,0,1,0]

b_major = [0,0,0,1,0,0,1,0,0,0,0,1]
b_minor = [0,0,1,0,0,0,1,0,0,0,0,1]

training_set_inputs = np.array([c_major, c_minor, db_major, cs_minor, d_major, d_minor, eb_major, ds_minor,
                                e_major, e_minor, f_major, f_minor, fs_major, fs_minor, g_major, g_minor,
                                ab_major, gs_minor, a_major, a_minor, bb_major, as_minor, b_major, b_minor])

training_set_outputs = np.array([[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]]).T
training_set_outputs_corr = training_set_outputs / 24
print(training_set_outputs_corr)
#training_set_outputs = np.array([[0,0,0,1,1,1,0,0,0,1,0,1,0,0,1,1,0,1,1,1,0,0,0,1]]).T

print ("Step 1) Print synaptic weights: ")
dumb_network.print_weights()

dumb_network.train_network(training_set_inputs, training_set_outputs_corr, 100000)

print ("Step 2) New synaptic weights after training: ")
dumb_network.print_weights()

print ("Step 3) Put into use ")
a = pitchClassesToInput(chord.pitchClasses)
hidden_state, output = dumb_network.compute(a)

print (output * 24)
