from dataclasses import dataclass


@dataclass
class Attribute:
    """Class that represents an attribute of a unit"""
    name: str
    description: str
    idx: int = -1

    def to_dict(self):
        return self.__dict__
