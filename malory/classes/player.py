from dataclasses import dataclass
from typing import List

from malory.classes.active_unit import ActiveUnit
from malory.orm.unit_orm import get_unit


@dataclass
class Player:
    """Class that represents a player"""
    units: List[ActiveUnit]
    idx: int = -1

    def __post_init__(self):
        self.data = {u.name: get_unit(u.name) for u in self.units}
        
    def to_dict(self):
        return {
            "units": [u.to_dict() for u in self.units],
            "data": [u.to_dict() for u in self.data]
        }
