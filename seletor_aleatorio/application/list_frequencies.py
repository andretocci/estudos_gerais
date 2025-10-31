from datetime import datetime
from typing import List, Tuple

from seletor_aleatorio.domain.model import Frequencias


def list_frequencies(frequencia_list: List[Frequencias]) -> Tuple[List[int], List[int]]:
    """ """
    freq_list = []
    id_list = []
    for i in frequencia_list:
        freq_list.append(i.get_frequencies())
        id_list.append(i.id)

    # The modified object is returned
    return id_list, freq_list
