import numpy as np

class NB:

    def __init__(self, prob_dict):
        self.p_yes = prob_dict["yes"]
        self.p_no = prob_dict["no"]
        self.probs = [np.array(i) for i in prob_dict["data"]]
        self.sample_count = prob_dict["total"]
        self.totals = []
        self.individual_prob = []
        self.unique_conditions = prob_dict["unique_values"]

        self.calc_totals()
        self.calc_individual_probs()

    def calc_totals(self):
        
        for prob in self.probs:
            total = []

            for column in range(prob.shape[1]):
                total.append(sum(prob[:, column]))

            self.totals.append(total)
        
        print(self.totals)

    def calc_individual_probs(self):

        for z, prob in enumerate(self.probs):
            prb = []

            for i in range(prob.shape[0]):

                for j in range(prob.shape[1]):
                    prb.append(self.probs[z][i, j] / self.totals[i][j])

                self.individual_prob.append(prb)

    @staticmethod
    def parse_data(data):
        prob_dict = {
            "yes": 0,
            "no": 0,
            "total": len(data),
            "original_data": [],
            "data": []
        }

        columns = len(data[0]) - 2
        total = len(data)
        yes = 0
        no = 0

        for row in data:
            
            if row[-1]:
                prob_dict["yes"] = prob_dict["yes"] + 1

        prob_dict["no"] = prob_dict["total"] - prob_dict["yes"]
        unique_values = []

        for column in range(columns + 1):
            unique = []

            for row in data:
                
                # creates a set to make sure all the values are unique
                if not row[column] in set(unique): 
                    unique.append(row[column])

            unique_values.append(unique)

        prob_arr = []

        prob_dict["unique_values"] = unique_values

        for i, unique in enumerate(unique_values):
            count = []
            operable_count = []
            yes_val_count = 0
            no_val_count = 0

            for val in unique:

                for row in data:
                    
                    if row[i] == val:

                        if row[-1]:
                            yes_val_count = yes_val_count + 1
                        else:
                            no_val_count = no_val_count + 1

                count.append([val, yes_val_count, no_val_count])
                operable_count.append([yes_val_count, no_val_count])
                yes_val_count = 0
                no_val_count = 0

            prob_dict["original_data"].append(count)
            prob_dict["data"].append(operable_count)

        print(prob_dict)
        return prob_dict

    def find_columns(self, conditions_arr):
        print("finding columns")
        probability_indexes = []

        for i, condition in enumerate(conditions_arr):
            
            if condition in self.unique_conditions[i]:
                
                for x, val in enumerate(self.unique_conditions[i]):

                    if val == condition:
                        print(val)
                        probability_indexes.append(x)
                        break
            else:
                raise Exception("Condition " + condition + "was not found")

        return probability_indexes
    
    def calculate_probabilities(self, condition_arr):
        probability_indexes = []
        yes_prob = 1
        no_prob = 1

        try:
            probability_indexes = self.find_columns(condition_arr)

            for prob in range(len(probability_indexes)):
                yes_prob = yes_prob * (self.probs[prob][probability_indexes[prob], 0] / self.p_yes)
                no_prob = no_prob * (self.probs[prob][probability_indexes[prob], 1] / self.p_no)

            yes_prob = yes_prob * (self.p_yes / self.sample_count)
            no_prob = no_prob * (self.p_no / self.sample_count)

            total = yes_prob + no_prob

            yes_prob = yes_prob / total
            no_prob = no_prob / total

            if yes_prob > no_prob:
                print("P(yes|" + str(condition_arr) + ") = " + str(yes_prob))
            else:
                print("P(no|)" + str(condition_arr) + ") = " + str(no_prob))

        except Exception as err:
            print(err)
    

prob_1 = [
    ["RAINY", "HOT", "HIGH", "WINDY", False],
    ["SUNNY", "HOT", "LOW", "NOT_WINDY", True],
    ["OVERCAST", "HOT", "HIGH", "NOT_WINDY", False],
    ["SUNNY", "COOL", "MILD", "NOT_WINDY", True],
    ["OVERCAST", "MILD", "HIGH", "WINDY", False],
]

nb = NB(NB.parse_data(prob_1))

nb.calculate_probabilities(["SUNNY", "HOT", "LOW", "NOT_WINDY"])
