import math
from dataclasses import dataclass
from typing import List, Tuple
from malory.classes.active_unit import ActiveUnit
from malory.classes.attack_parameters import AttackParameters
from malory.orm.unit_orm import get_unit
from malory.orm.user_orm import get_user_name


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
            "data": {name: u.to_dict() for name, u in self.data.items()},
            "idx": self.idx
        }

    def attack(self, unit_idx: int, username: str, other_idx: int, params: AttackParameters) -> Tuple[float, float]:
        """Resolves an attack between two units of different players"""
        from malory.orm.active_unit_orm import get_player, update_active_unit
        lst = list(filter(lambda x: x.idx == unit_idx, self.units))
        if not lst:
            raise AttributeError(f"No unit with index {unit_idx} was found for player {get_user_name(self.idx)}")
        unt = lst[0]
        p2 = get_player(username)
        lst = list(filter(lambda x: x.idx == other_idx, p2.units))
        if not lst:
            raise AttributeError(f"No unit with index {unit_idx} was found for player {username}")
        unt2 = lst[0]
        if unt2.men <= 0 or unt2.morale <= 0:
            raise ValueError("Invalid Target")
        data, other_data = unt.get_data(), unt2.get_data()

        damage = unt.attack(unt2, params)
        men_before = unt2.men
        pool = unt2.men * other_data.hitpoints
        pool = max(0.0, pool - damage)
        unt2.men = math.ceil(pool / other_data.hitpoints)
        if params.ranged:
            if unt.ammunition == 0:
                raise ValueError("No Ammunition")
            elif data.range == -1:
                raise ValueError("Unit has no range")
            unt.ammunition -= 1

        casualties = men_before - unt2.men
        if unt2.men > 0:
            morale = 1 + .5 * params.flank + .15 * data.has_attribute("Fearsome") - .15 * data.has_attribute(
                "Unbreakable")
            ratio = (men_before - unt2.men) / men_before + .5
            unt2.morale -= (men_before - unt2.men) * other_data.weight * ratio * morale
            unt2.morale = max(math.ceil(unt2.morale), 0)
        update_active_unit(unt)
        update_active_unit(unt2)
        return damage, casualties
