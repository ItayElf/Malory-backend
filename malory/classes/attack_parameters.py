from dataclasses import dataclass


@dataclass
class AttackParameters:
    ranged: bool = False
    flank: bool = False
    charge: bool = False
    advantage: int = 0
