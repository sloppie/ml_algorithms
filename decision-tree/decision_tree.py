import math
import numpy as np

from tree import Tree

"""
This class takes in the original data,
    @param_1: original_data
    @param_2 a multidimensional array of operable values in that data
    @param_3 max levels that the tree can go to (this is an optional arg)
The operable data is stored in a np.array and once its split, the original data and the operable row are both passed on to the child nodes in the tree
"""
class DecisionTree:

    def __init__(self, original_data, operable_data, max_levels=None):
        self.matrix = np.array(operable_data)
        print(self.matrix)
        self.data_arr = self.matrix.shape
        self.level = 0
        self.tree = Tree(original_data, operable_data, level=0, left=None, right=None)
        self.used_column = []
        self.max_levels = None

        if max_levels:
            self.max_levels = max_levels
        else:
            self.max_levels = self.matrix.shape[1]

    """
    This method is used to calculate the entropy based on the the matrix given in the decision tree
    It uses the self.used_colum to know which values not to navigate through
    This is used by the splitting function to know where to break the dat by
    """
    def calculate_entropy(self):
        unchecked = []
        entropies = []

        # this loop checks through the column array checkin for if it has been used
        for i in range(self.data_arr[1]):
            
            if i not in self.used_column:
                entropy = 0
                unique_values = []

                # get a count of each unique value in the matrix
                for value in self.matrix[:, i]:
                    index = find_value(unique_values, value)

                    # look for the value in the list
                    if index == -1:
                        new_val = {
                            "val": value,
                            "count": 1
                        }
                        unique_values.append(new_val)
                    else:
                        unique_values[index]["count"] = unique_values[index]["coundt"] + 1
                
                # calculate the entropy
                for value in unique_values:
                    # calculate entropy using e = p(value) * log2(p(value))
                    p_value = float(value["count"]) / float(self.matrix.shape[0])

                    if p_value != float(0):
                        entropy = entropy + (p_value * math.log(p_value, 2))

                new_entropy = {
                    "column_number": i,
                    "entropy": entropy
                }

                entropies.append(new_entropy)

        # compare_entropies to find the largest one
        largest_entropy = None

        for entropy in entropies:
                
            if not largest_entropy:
                largest_entropy = entropy
                continue

            if largest_entropy["entropy"] < entropy["entropy"]:
                largest_entropy = entropy

        self.used_column.append(largest_entropy["column_number"])

        return largest_entropy

    """
    This method is used to split the data using into two halves based on a condition.
    In an ideal situation, the function should have a column of first class function to be called to help split
    the data according to the respective column.
    This is not the case aas we use plai average to calculate the threshold that isused to split the data in the tree (self.tree)
    The level is passed to the tree to prevent spliting of data in the wrong level.
    If the maximum tree level is not declared, the method uses the column size as the maximum number of levels the self.tree can got to
    """
    def split_data(self):
        
        for i in range(self.max_levels): # finds the maximum number of times it can iterate base on the number of columns in the data
            largest_entropy = self.calculate_entropy()

            #column_values
            column_values = self.matrix[:, largest_entropy["column_number"]]
            column_sum = 0
            
            for x in column_values:
                column_sum = column_sum + x 

            column_average = column_sum / self.matrix.shape[0]

            self.tree.visit_node(column_average, self.level, largest_entropy['column_number'])
            self.level = self.level + 1

# works for the unique value dictionary
def find_value(arr, value):
    index = -1
    i = 0

    for val in arr:

        if val["val"] == value:
            index = i

            return index

        i = i + 1
    
    # the argument is that it will only get here if the value was not found
    return index

