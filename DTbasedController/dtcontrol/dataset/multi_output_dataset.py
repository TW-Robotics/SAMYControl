import numpy as np

from dtcontrol.dataset.dataset import Dataset
from dtcontrol.util import make_set

class MultiOutputDataset(Dataset):
    def __init__(self, filename):
        super().__init__(filename)
        self.tuple_ids = None
        self.tuple_id_to_tuple = None
        self.tuple_to_tuple_id = None
        self.unique_labels = None  # ids of lists of tuple ids
        self.list_id_to_list = None  # maps ids of lists of tuple ids to the actual lists of tuple ids
        # the data in a tuple (zipped) format where the outermost dimension becomes the innermost dimension
        # i.e. the new dimensions are: num_examples x num_labels x num_outputs
        self.tuples = None

    def compute_accuracy(self, y_pred):
        self.check_loaded()
        num_correct = 0
        for i in range(len(y_pred)):
            pred = y_pred[i]
            if pred is None:
                return None
            correct_tuples = set([tuple(l) for l in self.get_tuples()[i] if l[0] != -1])
            if set.issubset(make_set(pred), correct_tuples):
                num_correct += 1
        return num_correct / len(y_pred)

    def get_tuples(self):
        """
            Tensor of size (2, 4, 3), aka actions are of the type [y0 y1], there is for matching 4 states (X) and there is at most 3 possible undetermined actions
            For each ActionInput we get a matrix State-Possible values of the corresponding action input
            [ Y
             [ Action Input 0 -> Matrix (state x, array of 3 possible values for action input 0 due to undeterm)
              [ 0, -1, -1], State X[0], possible values of y0
              [ 0, -1, -1], State X[1], possible values of y0
              [ 0, -1, -1], State X[2], possible values of y0
              [ 1,  2,  0]  State X[3], possible values of y0
             ],
             [ Action Input 1 -> Matrix (state x, array of 3 possible values for action input 1 due to undeterm)
              [ 0, -1, -1], State X[0], possible values of y1
              [ 0, -1, -1], State X[1], possible values of y1
              [ 0, -1, -1], State X[2], possible values of y1
              [ 0,  0,  0]  State X[3], possible values of y1
             ]
            ]

            we stack in the axis 2 (undeterm.), hence we get: For each Possible Value(undet), a matrix State-ActionInputs (aka State-Action)

            [ Array of possible State-Actions
             [ State 0 X[0]
              [ 0  0], -> First Possible Action ([y0 y1]) for state X[0]
              [-1 -1], -> Second Possible Action ([y0 y1]) for state X[0]
              [-1 -1]  -> Third Possible Action ([y0 y1]) for state X[0]
             ],
             [ State 1 X[1]
              [ 0  0], -> First Possible Action ([y0 y1]) for state X[1]
              [-1 -1], -> Second Possible Action ([y0 y1]) for state X[1]
              [-1 -1]  -> Third Possible Action ([y0 y1]) for state X[1]
             ],
             [ State 2 X[2]
              [ 0  0], -> First Possible Action ([y0 y1]) for state X[2]
              [-1 -1], -> Second Possible Action ([y0 y1]) for state X[2]
              [-1 -1]  -> Third Possible Action ([y0 y1]) for state X[2]
             ],
             [ State 3 X[3]
              [ 1  0], -> First Possible Action ([y0 y1]) for state X[3]
              [ 2  0], -> Second Possible Action ([y0 y1]) for state X[3]
              [ 0  0]  -> Third Possible Action ([y0 y1]) for state X[3]
             ]
            ]
        """
        if self.tuples is None:
            self.tuples = np.stack(self.y, axis=2)
        return self.tuples

    def get_single_labels(self):
        return self.get_tuple_ids()

    def map_single_label_back(self, single_label):
        return self.map_tuple_id_back(single_label)

    def get_tuple_ids(self):
        """
        Maps each action [y0,...,ym] to an ID
        [ Array Y
         [ Set of non-deterministic actions available in x[0]
          [ 0  0],
          [-1 -1],
          [-1 -1]
         ],
         [ Set of non-deterministic actions available in x[1]
          [ 0  0],
          [-1 -1],
          [-1 -1]
         ],
         [ Set of non-deterministic actions available in x[2]
          [ 0  0],
          [-1 -1],
          [-1 -1]
         ],
         [ Set of non-deterministic actions available in x[3]
          [ 1  0],
          [ 2  0],
          [ 0  0]
         ]
        ]

         gets mapped to the following: The multiouput action with array [y0,...,ym]=[0 0] gets tuple id 2, [-1 -1] gets tuple id -1, [1 0] gets tuple id 3, [2 0] gets tuple id 4...
         [Set of non-deterministic actions available in X represented with the tuple ids
          [2 -1 -1],
          [2 -1 -1],
          [2 -1 -1],
          [3  4  2]
         ]
        """
        if self.tuple_ids is not None:
            return self.tuple_ids

        stacked_y_train = self.get_tuples() # Gets an array of states-Array of Possible Actions: stacked_y_train[0] is the state, stacked_y_train[1] is the action index among the possible actions, stacked_y_train[2] is the action,  and hence stacked_y_train.shape[2] is the size of an action )

        # default
        tuple_to_index = {tuple(-1 for i in range(stacked_y_train.shape[2])): -1} # Creates a dictionary element from tuple (action) to an index: 
                                                                                  # for example, for an action with two inputs: {(-1, -1) : -1 }

        self.tuple_ids = np.full((stacked_y_train.shape[0], stacked_y_train.shape[1]), -1) # Creates a matrix  size states x maximum number of possible actions filled with -1.
                                                                                           # In this matrix we will substitute every action tuple with its corresponding index, hence we will
                                                                                           # be able to handle multiouput label just as the single label output through indexes

        # first axis: datapoints
        # second axis: non-det
        # third axis: control inputs
        i = 0
        for datapoint in stacked_y_train: # For each state in X
            j = 0
            for action in datapoint: # For each possible action among the actions available in each state
                action_tuple = tuple(action)
                if action_tuple not in tuple_to_index.keys(): # If the actions does not have an index yet
                    # indexing from 1
                    tuple_to_index[action_tuple] = len(tuple_to_index) + 1 # Add the action (tuple) and its index to the dictionary
                self.tuple_ids[i][j] = tuple_to_index[action_tuple] # Sets in the matrix States-Actions the index of the action
                j += 1
            i += 1

        self.tuple_to_tuple_id = tuple_to_index # Dictionary that maps every action to a index
        self.tuple_id_to_tuple = {y: x for (x, y) in tuple_to_index.items()} # Dictionary that maps every index to the matching action tuple
        return self.tuple_ids # returns the matrix State-TupleIds (aka State-ActionIndex)

    def get_tuple_to_tuple_id(self):
        if self.tuple_to_tuple_id is None:
            self.get_unique_labels()
        return self.tuple_to_tuple_id

    def get_unique_labels(self):
        if self.unique_labels is None:
            self.unique_labels, self.list_id_to_list = self.get_unique_labels_from_2d(self.get_tuple_ids())
        return self.unique_labels

    def map_unique_label_back(self, label):
        l = self.list_id_to_list[label]
        return [self.tuple_id_to_tuple[i] for i in l if i != -1]

    def map_tuple_id_back(self, tuple_id):
        return self.tuple_id_to_tuple[tuple_id]

    def from_mask(self, mask):
        subset = MultiOutputDataset(self.filename)
        subset.copy_from_other_dataset(self)
        subset.parent_mask = mask
        subset.x = self.x[mask]
        subset.y = self.y[:, mask, :]
        if self.tuple_ids is not None:
            subset.tuple_ids = self.tuple_ids[mask]
            subset.tuple_id_to_tuple = self.tuple_id_to_tuple
            subset.tuple_to_tuple_id = self.tuple_to_tuple_id
        if self.unique_labels is not None:
            subset.unique_labels = self.unique_labels[mask]
            subset.list_id_to_list = self.list_id_to_list
        if self.tuples is not None:
            subset.tuples = self.tuples[mask]
        return subset

    def from_mask_optimized(self, mask):
        empty_object = type('', (), {})()
        empty_object.parent_mask = mask
        empty_object.get_single_labels = lambda: self.get_single_labels()[mask]
        return empty_object
