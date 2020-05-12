import numpy as np

class Centroid:

    def __init__(self, centroid_value):
        self.mean = centroid_value
        self.initial_member = centroid_value
        self.members = [centroid_value]

    def calculate_mean(self, new_member):
        self.members.append(new_member)

        member_mat = np.array(self.members)
        xs = np.array([[i] for i in member_mat[:, 0]]) # first column from each row
        ys = np.array([[i] for i in member_mat[:, 1]]) # second column from each row
        
        one = np.ones((1, xs.shape[0]))
        
        average_x = np.matmul(one, xs) / len(self.members)
        average_y = np.matmul(one, ys) / len(self.members)

        self.mean = [average_x[0, 0], average_y[0, 0]] # create the mean

    def reset(self):
        self.members = [self.members[0]]

    """
    The method returns an array of centroids initialised from the centroid class
    """
    @staticmethod
    def initialise_centroids(centroids):
        c_classes = []

        for centroid in centroids:
            # TODO create a centroid class that hosts the means
            c_classes.append(Centroid(centroid))

        return c_classes
