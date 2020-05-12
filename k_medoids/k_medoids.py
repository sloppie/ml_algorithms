import numpy as np
from random import randint


# K Medoids
class KM:

    def __init__(self, points, k, trials=2):
        self.points = points
        self.trials = trials
        self.medoids = KM.find_medoids(points, k, trials)
        self.k = k

    """
    This method finds the Manhattan distance i.e: |x1 - x2| + |y1 - y2|
    params:
        @param_1 the matrix of points
        @param_2 the matrix of medoids

    returns:
        it returns a matrix containing the manhattan distances in columns of each
        unique point row by row
        all the distances for point p1 are located in row 1, with each column representing
        each respective medoid.
    """
    def find_manhattan_distance(self, points, medoids):
        """
        Crries out matrix multiplication between all the respective points p and
        the transposed medoids matrix.
        This produces a matrix of each row p, and the columns representing each medoid m
        thus returning a matrix of [p x m].
        This matrix will enable cheap calculation of cost
        """
        distances = np.matmul(points, medoids.transpose())

        return distances

    """
    This method clusters the points according to the manhattan distances based on the medoids
    """
    def classify_data(self):
        epochs = []

        for medoid in self.medoids:
            new_points, medoid_matrix = KM.remove_medoids(self.points, medoid)
            distances = self.find_manhattan_distance(new_points, medoid_matrix)
            
            results = {
                "medoids": medoid_matrix[:, :],
                "epoch": [],
                "epoch_cost": 0
            }

            medoid_array = medoid_matrix[:, :]
            epoch = []
            epoch_cost = 0 # keeps trck of the total minumum_cost

            # create a column for each unique medoid
            for i in range(self.k):
                epoch.append([])

            
            for i in range(new_points.shape[0]):
                # stores the distance value in index 0, and the column_number in index 1
                smallest = []

                for j in range(distances.shape[1]):

                    if len(smallest) == 0:
                        smallest = [distances[i, j], j]
                    elif smallest[0] > distances[i, j]:
                        smallest = [distances[i, j], j]
                
                epoch[smallest[1]].append(new_points[i, :])
                epoch_cost = epoch_cost + smallest[0] #adds to the minimum cost

            # appends an array whose first index contains the all the points and their 
            # distribution. the second index contains the cost for that epoch
            results["epoch"] = epoch
            results["epoch_cost"] = epoch_cost
            epochs.append(results)

        return epochs

    def find_smallest_cost(self):
        epochs = self.classify_data()

        smallest_cost = None

        for epoch in epochs:
            
            if smallest_cost:
                
                if epoch["epoch_cost"] < smallest_cost["epoch_cost"]:
                    smallest_cost = epoch
            else:
                smallest_cost = epoch

        return smallest_cost

    """
    This static method returns a multidimensional array containing the medoids to be
    used on each trial.
    These medoids are unique and this method tries to prevent re-use of a medoid
    params:
        @param_1 is the point matrix passed to the KM class
        @param_2 k is the number of medoids the user wants
        @param_3 is the number of trials the user wants to run
    """
    @staticmethod
    def find_medoids(points, k, trials):
        medoids = []
        used_medoids = []

        def generate_medoids():
            values = []

            # used to generate "k" random values 
            for val in range(k):
                random_val = randint(0, points.shape[0] - 1) # upper bound being the number of rows in the points data
                
                if random_val in values:

                    while random_val in values:
                        random_val = randint(0, points.shape[0] - 1)

                    values.append(random_val)
                else:
                    values.append(random_val)
            
            return values

        # generate new medoids for each trial
        for t in range(trials):
            medoid = generate_medoids()

            #recurses if medoid is already found
            if medoid in used_medoids:

                while medoid in used_medoids:
                    medoid = generate_medoids()

            used_medoids.append(medoid)
            medoids.append(medoid)

        return medoids

    """
    This static method returns a matrix of new_points with the medoid points removes
    it also returns the matrix of the medoid points of respective to the trial
    params:
        @param_1 is the original points passed to the KM
        @param_2 is an array containing the medoids indexes
    """
    @staticmethod
    def remove_medoids(points, medoids):
        new_points = []
        medoid_points = []

        for i in range(points.shape[0]):
            
            if not i in medoids:
                new_points.append(points[i, :])
            else:
                medoid_points.append(points[i, :])

        new_points = np.array(new_points)
        medoid_points = np.array(medoid_points)

        return [new_points, medoid_points]
    
    @staticmethod
    def print_cluster(cluster):
        clusters = cluster["epoch"]

        cluster_matrices = []

        for cl in clusters:
            cluster_matrices.append(np.array(cl))

        i = 0

        # print the clusters with the respective medoid
        for medoid in cluster["medoids"]:
            print("Medoid: ")
            print(medoid)
            print("cluster: ")
            print(cluster_matrices[i])

            i = i + 1
        
        print("cost: " + str(cluster["epoch_cost"]))

