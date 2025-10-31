from datetime import datetime

from seletor_aleatorio.domain.model import Frequencias


def add_new_win(frequencia_item: Frequencias) -> Frequencias:
    """
    Adds today's date to the dates list of a Frequencias item.
    This is the "business logic" for adding a winner.
    """
    today_str = datetime.today().strftime("%Y-%m-%d")
    if today_str not in frequencia_item.dates:
        frequencia_item.dates.append(today_str)

    # The modified object is returned
    return frequencia_item
