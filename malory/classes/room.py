from dataclasses import dataclass
from typing import Optional

from malory.classes.player import Player


@dataclass
class Room:
    """Class that represents a game room"""
    name: str
    points: int
    player1: Player
    player2: Optional[Player] = None

    def to_dict(self):
        return {
            **self.__dict__,
            "player1": self.player1.to_dict(),
            "player2": None if not self.player2 else self.player2.to_dict()
        }
