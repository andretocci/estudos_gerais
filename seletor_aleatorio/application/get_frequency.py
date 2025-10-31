from datetime import datetime
from typing import List, Optional

from seletor_aleatorio.domain.model import Frequencias


def get_frequency_by_id(
    item_id: int, frequency_list: List[Frequencias]
) -> Optional[Frequencias]:
    """
    Finds a single Frequencias item from a list based on its ID.

    Args:
        item_id: The ID to search for.
        frequency_list: The list of Frequencias objects to search within.

    Returns:
        The matching Frequencias object, or None if not found.
    """
    for item in frequency_list:
        if item.id == item_id:
            return item

    return None  # Explicitly return None if no match is found
