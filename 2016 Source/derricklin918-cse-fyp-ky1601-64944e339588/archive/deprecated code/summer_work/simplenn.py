import numpy as np

class NeuronLayer:
    def __init__(self, number_of_inputs_per_neuron, number_of_neurons):
        self.syn_weight = 2 * np.random.random((number_of_inputs_per_neuron, number_of_neurons)) - 1

class NeuralNetwork:
    def __init__(self, layer1, layer2):
        self.hidden_layer = layer1
        self.output_layer = layer2

    def activation(self, x, deriv = False):
        if (deriv == True):
            return x * (1 - x)

        return 1 / (1 + np.exp(-x))

    def train_network(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for i in range(number_of_training_iterations):

            hidden_layer_output, output_layer_output = self.compute(training_set_inputs)

            output_layer_error = training_set_outputs - output_layer_output
            output_layer_delta = output_layer_error * self.activation(output_layer_output, True)

            hidden_layer_error = output_layer_delta.dot(self.output_layer.syn_weight.T)
            hidden_layer_delta = hidden_layer_error * self.activation(hidden_layer_output, True)

            hidden_layer_adjustment = training_set_inputs.T.dot(hidden_layer_delta)
            output_layer_adjustment = hidden_layer_output.T.dot(output_layer_delta)

            self.hidden_layer.syn_weight += hidden_layer_adjustment
            self.output_layer.syn_weight += output_layer_adjustment

    def compute(self, training_set_inputs):
        hidden_layer_output = self.activation(np.dot(training_set_inputs, self.hidden_layer.syn_weight))
        output_layer_output = self.activation(np.dot(hidden_layer_output, self.output_layer.syn_weight))
        return hidden_layer_output, output_layer_output

    def print_weights(self):
        print ("    Hidden Layer (24 neurons, each with 12 inputs): ")
        print (self.hidden_layer.syn_weight)
        print ("    Output Layer (1 neuron, with 24 inputs):")
        print (self.output_layer.syn_weight)

if __name__ == "__main__":

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

    print ("Stage 1) Random starting synaptic weights: ")
    dumb_network.print_weights()

    dumb_network.train_network(training_set_inputs, training_set_outputs_corr, 100000)

    print ("Stage 2) New synaptic weights after training: ")
    dumb_network.print_weights()

    # Test the neural network with a new situation.
    print ("Stage 3) Considering a new situation ")
    hidden_state, output = dumb_network.compute(np.array([1,0,0,0,1,0,0,0,0,0,0,0]))

    print (output * 24)
