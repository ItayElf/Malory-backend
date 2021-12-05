from dataclasses import dataclass
from malory.classes.unit import Unit
from malory.orm.unit_orm import get_unit


@dataclass
class ActiveUnit:
    """Class that represents an active unit (a unit that is in game rather than plain data)"""
    name: str
    men: int
    morale: int
    ammunition: int
    idx: int = -1

    def to_dict(self):
        return self.__dict__

    def get_data(self) -> Unit:
        return get_unit(self.name)

    @classmethod
    def active_unit_from_datasheet(cls, unit: Unit):
        return cls(unit.name, unit.men, unit.morale, unit.ammunition)


