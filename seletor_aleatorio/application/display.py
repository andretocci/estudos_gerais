import time
import sys
from IPython.display import Image, display


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
