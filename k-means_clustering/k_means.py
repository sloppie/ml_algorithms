import numpy as np
from random import randint

from centroid import Centroid

class KMC:

    def __init__(self, points, k, max_trials=5):
        self.points = points
        self.k = k
        self.max_trials = max_trials
        self.centroids = KMC.find_centroids(points, k, max_trials)
        self.new_points = KMC.remove_centroids(self.points, self.centroids)
        # generate the centroids
        self.centroids = self.generate_centroids(self.points, self.centroids)

    def generate_centroids(elf, points, centroids):
        cntrds = KMC.generate_centroid_points(points, centroids)
        centroids_by_trial = [Centroid.initialise_centroids(cntrd) for cntrd in cntrds]
        
        return centroids_by_trial

    def find_ed(self, new_points, centroids):
        resultant_matrix = None
        
        e_distances = []

        # create a matrix fro each centroid with the same row size as the points
        for index, centroid in enumerate(centroids):
            centroid_matrix = np.array([centroid.mean for i in range(new_points.shape[0])])
            eucledian_distance = centroid_matrix - new_points
            eucledian_distance = eucledian_distance * eucledian_distance
            ones = np.ones([2, 1])

            eucledian_distance = np.matmul(eucledian_distance, ones)

            # this distances are added as an array which would translate to a column, thus after all are appended
            # to the e_distances matrix, there is the need to transpose the matrix, so as to have the 
            # eucledian distances of each point respective to a centroid in the same row
            ed_column = []

            for i in eucledian_distance[:, :]:
                ed_column.append(i[0])

            e_distances.append(ed_column)

        # create a matrix and then transpose it
        """
        this creates a matrix that looks like this:
            [eucledian distances for point 1],
            [eucledian distances for point 2],
            ...
            [eucledian distances for point n]
        each column in the matrix represents the respective centroid
        """
        e_distances = np.array(e_distances).transpose()

        resultant_matrix = e_distances

        return resultant_matrix

    """
    Given the data, this method returns an array of matrices of how the data should be clustered
    based on the eucledian distances passed to the method.
    This function also aleters the mean of each cluster
    Params:
        @param_1 is the eucledian distances
    """
    def cluster_data(self, new_points, e_distances):

        for i in range(e_distances.shape[0]):
            least = None

            # find the least distance
            for j in range(e_distances.shape[1]):

                if least:
                    
                    if e_distances[i, j] < least["distance"]:
                        least["distance"] = e_distances[i, j]
                        least["column"] = j

                else:
                    least = {
                        "column": j,
                        "distance": e_distances[i, j]
                    }

            # add new member to the centroid with the least distance
            self.centroids[self.active_index][least["column"]].calculate_mean(new_points[i, :]) # passes the point to the centroid

        # create a list of the new clusters
        new_cluster = []

        for centroids in self.centroids[self.active_index]:
            cluster = []
            new_matrix = None

            if len(centroids.members) > 1:
                new_matrix = np.array(np.array(centroids.members)[1:, :])

                centroids.reset() # reset the centroid cluster

                new_cluster.append(new_matrix)

        return new_cluster

    def run(self):

        for index, centroids in enumerate(self.centroids):
            self.active_index = index

            # first initialise the previous cluster to a bunch of zeros matrices
            previous_cluster = []
        
            for i in centroids:
                previous_cluster.append(np.zeros(self.new_points[index].shape))

            # define cluster process function to avoid repeating code
            def cluster_data():
                e_distances = self.find_ed(self.new_points[index], centroids)
                new_cluster = self.cluster_data(self.new_points[index], e_distances)

                return new_cluster

            COUNT = 0
            # run initial cluster
            new_cluster = cluster_data()

            # loop until the new_cluster and previous_cluster are similar
            while not compare_clusters(new_cluster, previous_cluster):
                # !TODO create a global list that keeps track of previous clusters
                previous_cluster = new_cluster # reassign previous cluster
                new_cluster = cluster_data()

                if COUNT == 100:
                    previous_cluster = new_cluster
                    break
                else:
                    COUNT = COUNT + 1

            print("final cluster: ")
            for cluster, centroid in zip(previous_cluster, centroids):
                print("cluster for centroid: " + str(centroid.initial_member))
                print(cluster)


    """
    This static method returns a multidimensional array containing the centroids to be
    used on each trial.
    These medoids are unique and this method tries to prevent re-use of a medoid
    params:
        @param_1 is the point matrix passed to the KMC class
        @param_2 k is the number of centroids the user wants
        @param_3 is the number of trials the user wants to run
    """
    @staticmethod
    def find_centroids(points, k, trials):
        centroids = []
        used_centroids = []

        def generate_centroids():
            values = []

            # used to generate "k" random values 
            for val in range(k):
                random_val = randint(0, len(points) - 1) # upper bound being the number of rows in the points data
                
                if random_val in values:

                    while random_val in values:
                        random_val = randint(0, len(points) - 1)

                    values.append(random_val)
                else:
                    values.append(random_val)
            
            return values

        # generate new medoids for each trial
        for t in range(trials):
            centroid = generate_centroids()

            #recurses if medoid is already found
            if centroid in used_centroids:

                while centroid in used_centroids:
                    centroid = generate_centroids()

            used_centroids.append(centroid)
            centroids.append(centroid)

        return centroids

    @staticmethod
    def generate_centroid_points(points, centroids):
        trials = []

        for trial in centroids:
            new_points = []

            for centroid_row in trial:
                new_points.append(points[centroid_row])

            trials.append(new_points)

        return trials
    
    """
    Returns a numpy array of the points without the centroid points
    """
    @staticmethod
    def remove_centroids(points, trials):
        pbt = []

        for centroids in trials:
            new_points = []

            for index, point in enumerate(points):
                found = False

                if not index in centroids:
                    new_points.append(point)

            pbt.append(np.array(new_points))

        return pbt



# compare two centroid clusters
def compare_clusters(c1, c2):
    # compare outer length
    length = len(c1) == len(c2)
    similar = True

    for c1_points, c2_points in zip(c1, c2):
        # since the inner clusters are stored ass matrices, we can use the
        # numpy matrix comparison functions to compare
        similar = np.array_equal(c1_points, c2_points)

        if not similar:
            break

    return length and similar


if __name__ == "__main__":
    points = [
        [2, 3],
        [10, 20],
        [3, 4],
        [20, 10],
        [7, 8],
        [3, 2],
        [6, 8],
        [8, 6],
        [7, 6],
        [9, 8],
        [8, 9]
    ]
    kmc = KMC(points, 2, 10)

    kmc.run()

