import logging

import numpy as np
import pandas as pd

from dtcontrol.dataset.dataset_loader import DatasetLoader

class CSVDatasetLoader(DatasetLoader):
    def _load_dataset(self, filename):
        with open(filename, 'r') as f:
            logging.info(f"Reading from {filename}")
            f.readline()  # whether permissive

            state_dim, input_dim = map(int, f.readline().split("BEGIN")[1].split())

            ds = pd.read_csv(f, header=None)

            unique_list = []
            for i in range(state_dim, state_dim + input_dim): # for each action input
                unique_list += ds[i].unique().tolist() # extracts the unique values that each action input can take and places it in a list (the value can appear more than once in the list if appears in different action inputs)
            index_to_actual = {x + 1: y for x, y in enumerate(set(unique_list))} # Dictionary that assigns an integer index to each possible different input value (now appearing only once) 
            value_to_index = {y: x for x, y in index_to_actual.items()} # Reverse dictionary of index_to_actual (so to each different action input value gives the integer index)
            ds[[i for i in range(state_dim, state_dim + input_dim)]] = ds[
                [i for i in range(state_dim, state_dim + input_dim)]].applymap(lambda x: value_to_index[x]) # Rewrites the input actions with the integer indexes previously computed

            # It works on the data to compute different possible actions (using integer indexes) for the same state. Each state appear now only once, and the undeterministic possible inputs for each input of the action appear listed using the integer indexes
            grouped = ds.groupby([i for i in range(state_dim)], sort=False)
            aggregate = grouped[state_dim].apply(list).reset_index(name=state_dim)
            for i in range(1, input_dim):
                aggregate[state_dim + i] = grouped[state_dim + i].apply(list).reset_index(name=state_dim + i)[
                    state_dim + i]

            max_non_det = aggregate[state_dim].agg(len).max() # Computes maximal number of (undeterm.) possible inputs

            # Fills every input action list of possible values with -1, so all the arrays in the input actions have the same length
            for i in range(0, input_dim):
                aggregate[state_dim + i] = aggregate[state_dim + i].apply(
                    lambda ls: ls + [-1 for i in range(max_non_det - len(ls))])

            x = np.array(aggregate[[i for i in range(state_dim)]]) # creates X (every state only appears once)

            # Creates the "3D-Matrix" ("Cube"/"Tensor") Y ActionInput-State-PossibleValuesIndexes
            if input_dim > 1:
                y = np.ndarray((input_dim, x.shape[0], max_non_det), dtype=np.int16)
                for i in range(input_dim):
                    y[i] = np.array(aggregate[state_dim + i].tolist())
            else:
                y = np.array(aggregate[state_dim].tolist())

            # construct metadata
            # assumption is that UPPAAL only works with integers
            x_metadata = dict()
            x_metadata["variables"] = [f"x_{i}" for i in range(state_dim)]
            x_metadata["categorical"] = []
            x_metadata["min_inner"] = x_metadata["min_outer"] = [float(i) for i in np.amin(x, axis=0)]
            x_metadata["max_inner"] = x_metadata["max_outer"] = [float(i) for i in np.amax(x, axis=0)]
            x_metadata["step_size"] = None  # todo

            y_metadata = dict()
            y_metadata["variables"] = [f"u_{i}" for i in range(input_dim)]
            y_metadata["min"] = [min(index_to_actual.values())]
            y_metadata["max"] = [max(index_to_actual.values())]
            y_metadata["step_size"] = None  # todo

            logging.debug(x_metadata)
            logging.debug(y_metadata)

            return (x, x_metadata, y, y_metadata, index_to_actual)
