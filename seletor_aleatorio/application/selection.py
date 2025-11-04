import random

import numpy as np


def weighted_random_selection(data, debug=False):
    """
    Selects a name from a dictionary of names and frequencies.
    The probability of a name being selected is inversely proportional to its frequency.

    Args:
        data (dict): A dictionary where keys are names (str) and
                     values are their frequencies (int/float).

    Returns:
        str: The randomly selected name.
        Returns None if the input data is empty.
    """
    if not data:
        print("Input data is empty.")
        return None

    # Separate the names (population) and their frequencies
    names = list(data.keys())
    frequencies = np.array(list(data.values()))
    total_freq = frequencies.sum()
    probabilities = frequencies / total_freq
    inverse_weights = 1 / probabilities
    inverse_weights = inverse_weights / inverse_weights.sum()

    if debug:
        print(frequencies, total_freq)
        print(probabilities)
        print(inverse_weights)

    selected_name = np.random.choice(names, p=inverse_weights)

    return selected_name, inverse_weights
