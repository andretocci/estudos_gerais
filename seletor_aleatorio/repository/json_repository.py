import json
from typing import List
from seletor_aleatorio.domain.model import Frequencias

# Define a default path, which is cleaner
DEFAULT_FILE_PATH = "frequencies.json"


def save_frequencies(registros: List[Frequencias], path: str = DEFAULT_FILE_PATH):
    """
    Saves a list of Frequencias models to a JSON file.
    """
    data = [reg.model_dump() for reg in registros]

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except IOError as e:
        print(f"Error saving file to {path}: {e}")
        return False


def load_frequencies(path: str = DEFAULT_FILE_PATH) -> List[Frequencias]:
    """
    Loads a list of Frequencias models from a JSON file.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [Frequencias(**item) for item in data]

    except FileNotFoundError:
        print(f"File not found at {path}. Returning empty list.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {path}. Returning empty list.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
