import numpy as np

class Adeline:

    def __init__(self, weight_size, training_set, learning_rate):
        self.weights = np.random.randn(weight_size, 1)
        self.bias = np.array([[1.0] for i in training_set[0][1]])
        self.training_set = training_set
        self.learning_rate = learning_rate

    def generate_output(self, inputs):
        return np.matmul(inputs.transpose(), self.weights)

    def calculate_error(self, output, target):
        return target - output

    def adjust_weights(self, inputs, error):
        self.weights = self.weights + ((self.learning_rate) * error * inputs)

    def train(self):

        for data in self.training_set:
            inputs = np.array([[i] for i in data[0]])
            target = np.array([[i] for i in data[1]])
            
            output = self.generate_output(inputs)
            error = self.calculate_error(inputs, target)
            self.adjust_weights(output, error)


