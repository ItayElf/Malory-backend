from dataclasses import dataclass


@dataclass
class Attribute:
    """Class that represents an attribute of a unit"""
    name: str
    description: str
    idx: int = -1
