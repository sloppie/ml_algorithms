import numpy as np
import adeline as ad

def run_test(training_range, learning_rate):
    training_data = []

    for i in range(training_range):

        #if i % 4 == 0:
        #    training_data.append([[-1.0, -1.0], [-1.0]])
        #elif i % 4 == 1:
        #    training_data.append([[-1.0, 1.0], [1.0]])
        #elif i % 4 == 2:
        #    training_data.append([[1.0, -1.0], [1.0]])
        #elif i % 4 == 3:
        #    training_data.append([[1.0, 1.0], [-1.0]])
        training_data.append([[1.0, 1.0], [-1.0]])

    net = ad.Adeline(2, training_data, learning_rate)
    net.train()

    for i in range(4):

        if i % 4 == 3:
            print(net.generate_output(np.array([[i] for i in [1.0, 1.0]])))
