import numpy as np

from k_medoids import KM

dummy_data = [
    [20, 3],
    [3, 20],
    [4, 5],
    [7, 2],
    [2, 7],
    [10, 17],
    [3, 4],
    [5, 6]
]

point_matrix = np.array(dummy_data)

# print(KM.find_medoids(point_matrix, 4, 3))
smallest_epoch = KM(point_matrix, 2, 5).find_smallest_cost()

KM.print_cluster(smallest_epoch)
