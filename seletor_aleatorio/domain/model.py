from pydantic import BaseModel
from typing import List


class Frequencias(BaseModel):
    """
    Represents the data model for frequency tracking.
    """

    id: int
    name: str
    alias: str
    dates: List[str]
    balanceamento: int

    def get_frequencies(self) -> int:
        """Calculates the total frequencies."""
        return len(self.dates) + self.balanceamento

    def get_name(self) -> str:
        if self.alias is None:
            alias = ""
        if len(self.alias) < 1:
            alias = ""
        else:
            alias = " - " + self.alias
        return self.name + alias
