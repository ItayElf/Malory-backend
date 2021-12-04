from dataclasses import dataclass
from malory.classes.attribute import Attribute
from typing import List


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

