class Tree:

    def __init__(self, original_data, data, **kwargs):
        self.original_data = original_data
        self.data = data
        self.right = None
        self.left = None
        # the threshold will be used when classifying new data based on what the model has learnt
        self.threshold = None
        self.column_number = None

        if kwargs['level'] is not None:
            self.level = kwargs['level']
        else:
            self.level = 0

        if kwargs['left'] is not None:
            self.left = kwargs['left']

        if kwargs['right'] is not None:
            self.right = kwargs['right']

    def add_node(self, node):
        
        if not self.has_left() or not self.has_right():

            if not self.has_left():
                self.left = node
            else:
                self.right = node
        else:
            raise Exception("The Node is already full")

    def has_left(self):
        return self.left is not None

    def has_right(self):
        return self.right is not None

    """
    This method is used to carry out the splitting of the tree based on the threshold passed to it
    The level heps prevent slitting happenning to node that is not on the same level
    as the decision tree is operating on.
    The column number helps to to usee the correct column in the data when asessing whether or not to split it
    if the data is splitable, the data storee the threshold and the column_number at which the data was split to allow correct classification
    after the model is trained.
    The Left child: stores values les than or equal to the threshold
    The right child: stores values greater than the threshold
    !NOTE: if upon trying to split, one of the sides ends up empty, the data is not split any further and thus no new nodes are created
    """
    def visit_node(self, threshold, level, column_number):

        if(level == self.level):
            original_left = []
            new_left = []
            original_right = []
            new_right = []

            count = 0 # used to keep track of the original data

            for i in self.data:
                
                if i[column_number] <= threshold:
                    #keep a copy of the original data
                    original_left.append(self.original_data[count])
                    new_left.append(i)
                else:
                    original_right.append(self.original_data[count])
                    new_right.append(i)

                count = count + 1

            if len(new_left) == 0 or len(new_right) == 0:
                print("This function could not be split any further")
            else:
                # add the node threshold to help classify new data from the model
                self.threshold = threshold
                #add the column number used to split this data
                self.column_number = column_number

                #create the children to this node
                self.add_node(Tree(
                    original_left,
                    new_left,
                    level=(level + 1),
                    left=None,
                    right=None
                ))

                # add the right subsequently
                self.add_node(Tree(
                    original_right,
                    new_right,
                    level=(level + 1),
                    left=None,
                    right=None
                ))

        elif self.level < level:
            
            if self.has_left():
                self.left.visit_node(threshold, level, column_number)

            if self.has_right():
                self.right.visit_node(threshold, level, column_number)
    
    # basic recursive printing of trees
    def print_tree(self):
        
        if not self.has_right() and not self.has_left():
            print(self.level)
            # print(self.data)
        else:
            print('if value <= ' + str(self.threshold) + ": ")

            if self.has_left():
                self.left.print_tree()

            print("else:")

            if self.has_right():
                self.right.print_tree()
        
