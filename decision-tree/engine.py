import numpy as np

import decision_tree as dt

# read in data
dummy_data = np.random.rand(100, 5)
dummy_data = 100 * dummy_data # spread out the values over a hundred

model = dt.DecisionTree(
    dummy_data[:, :],
    dummy_data[:, 1:], # all rows, but the first column containing ids is exempted
)

model.split_data()
model.tree.print_tree()
