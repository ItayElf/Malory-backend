from __future__ import annotations

from dataclasses import dataclass

from malory.classes.attack_parameters import AttackParameters
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

    def get_modifier(self, other: ActiveUnit, params: AttackParameters) -> float:
        """Returns modifier for the attack based on the params"""
        data, other_data = self.get_data(), other.get_data()
        m = 1 + .25 * params.advantage
        m += .25 * params.flank
        m += (data.charge / 100) * params.charge
        if data.has_attribute("Polearm") and "Cavalry" in other_data.clas:
            m += .25
        if data.has_attribute("Anti-Armor") and "Heavy" in other_data.clas:
            m += .25
        if data.has_attribute("Flank Experts"):
            m += .25 * params.flank
        return m

    def attack(self, other: ActiveUnit, params: AttackParameters) -> float:
        """Returns calculated damage of an attack"""
        data, other_data = self.get_data(), other.get_data()
        weapon_damage = data.ranged_damage if params.ranged else data.damage
        ap = max(0, data.ranged_ap if params.ranged else data.ap)
        shield = 1 - other_data.shield if params.ranged and other_data.shield > 0 else 1
        damage_per_hit = ((weapon_damage ** 2) / (2 * other_data.armor)) * shield + ap
        attack_skill = data.ranged_attack if params.ranged else data.melee_attack
        hits = self.men * min(1.0, attack_skill / other_data.defense)
        m = self.get_modifier(other, params)
        return round(damage_per_hit * hits * m, 2)

    @classmethod
    def from_datasheet(cls, unit: Unit):
        return cls(unit.name, unit.men, unit.morale, unit.ammunition)


if __name__ == '__main__':
    unt1 = ActiveUnit.from_datasheet(get_unit("Axemen"))
    unt2 = ActiveUnit.from_datasheet(get_unit("Heavy Spearmen"))
    print(unt1.attack(unt2, AttackParameters()))
