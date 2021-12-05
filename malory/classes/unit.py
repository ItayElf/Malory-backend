from dataclasses import dataclass
from malory.classes.attribute import Attribute
from typing import List, Union


@dataclass
class Unit:
    """Class that represents a unit data sheet"""
    category: str
    name: str
    description: str
    clas: str
    subclass: str
    cost: float
    men: int
    weight: float
    hitpoints: int
    armor: int
    shield: float
    morale: int
    speed: int
    melee_attack: int
    defense: int
    damage: int
    ap: int
    charge: int
    ammunition: int
    range: int
    ranged_attack: int
    ranged_damage: int
    ranged_ap: int
    attributes: List[Attribute]
    idx: int = -1

    def to_dict(self):
        return {
            **self.__dict__,
            "attributes": [attr.to_dict() for attr in self.attributes]
        }

    def has_attribute(self, attr: Union[str, Attribute]) -> bool:
        """Returns true if a unit has the given attribute"""
        if isinstance(attr, Attribute):
            attr = attr.name
        return any([a.name == attr for a in self.attributes])

