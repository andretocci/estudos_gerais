import random
import time
import sys
from IPython.display import Image, display

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


def print_probabilities(names, weights):
    print("_______________________")
    print("--- Probabilidades ---")
    print("----------------------")
    for name, weight in zip(names, weights):
        max_str = max([len(name) for name in names])
        print(f"{name + (" " * (max_str - len(name) ))}:|{"|" * int(weight * 100)}")
    print("_______________________")


def suspense_selection(selected, delay=0.5, suspense_steps=5, img_pah=None):
    """
    Creates a suspense effect before revealing a randomly selected name.

    Args:
        selected (list): selected name.
        delay (float): Delay in seconds between suspense steps.
        suspense_steps (int): Number of suspense steps before revealing.

    Returns:
        str: The selected name.
    """
    print("Preparando para o sorteio...")
    # Load your gif using matplotlib

    # Loading the gif into our Jupyter notebook
    if img_pah is not None:
        try:
            display(Image(img_pah))
        except Exception as e:
            print(e)
    for i in range(suspense_steps):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(delay)
    print("\nE o selecionado é...")
    time.sleep(1)
    print(f"!!! {selected} !!!")
    return selected
