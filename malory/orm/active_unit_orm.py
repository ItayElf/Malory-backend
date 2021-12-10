import sqlite3
from typing import List

from malory.classes.active_unit import ActiveUnit
from malory.classes.player import Player
from malory.orm.unit_orm import get_unit
from settings import DB_LOCATION

get_player_sql = """SELECT u.username, u.id, group_concat(au.id), group_concat(au.name), group_concat(au.men), group_concat(au.morale), group_concat(au.ammunition)
FROM users u
LEFT JOIN active_units au ON au.player_id = u.id
WHERE u.username = ?
GROUP BY u.username;"""


def add_active_unit(unit_name: str, player_id: int) -> bool:
    """Adds an active unit to a player's army, returning true if the insertion was successful"""
    try:
        unit = ActiveUnit.active_unit_from_datasheet(get_unit(unit_name))
        with sqlite3.connect(DB_LOCATION) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=?", (player_id,))
            if not c.fetchone():  # No player with that id
                return False
            conn.execute("INSERT INTO active_units(name, men, morale, ammunition, player_id) VALUES(?, ?, ?, ?, ?)",
                         (unit.name, unit.men, unit.morale, unit.ammunition, player_id))
            conn.commit()
            return True
    except AttributeError:  # No unit was found
        return False


def get_active_unit(idx: int) -> ActiveUnit:
    """Returns an active unit of a player"""
    with sqlite3.connect(DB_LOCATION) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM active_units WHERE id=?", (idx,))
        tup = c.fetchone()
        if not tup:
            raise AttributeError(f"No active unit was found with index {idx}")
        idx, name, men, morale, ammunition, player_id = tup
        return ActiveUnit(name, men, morale, ammunition, idx)


def delete_active_unit(idx: int) -> bool:
    """Deletes an active unit and returns true if successful"""
    with sqlite3.connect(DB_LOCATION) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM active_units WHERE id=?", (idx,))
        if not c.fetchone():
            return False
        conn.execute("DELETE FROM active_units WHERE id=?", (idx,))
        conn.commit()
        return True


def get_player_army(player_idx: int) -> List[ActiveUnit]:
    """Returns a list of all active units that a player has"""
    with sqlite3.connect(DB_LOCATION) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM active_units WHERE player_id=?", (player_idx,))
        lst = c.fetchall()
        return [ActiveUnit(name, men, morale, ammunition, idx) for (idx, name, men, morale, ammunition, player_id) in
                lst]


def active_unit_owner(unit_idx: int) -> int:
    """Return player id of a unit"""
    with sqlite3.connect(DB_LOCATION) as conn:
        c = conn.cursor()
        c.execute("SELECT player_id FROM active_units WHERE id=?", (unit_idx,))
        tup = c.fetchone()
        if not tup:
            raise AttributeError(f"No unit was found with index {unit_idx}")
        return tup[0]


def get_player(username: str) -> Player:
    """Returns a player object based on a username, throwing an attribute error if player does not exist"""
    with sqlite3.connect(DB_LOCATION) as conn:
        c = conn.cursor()
        c.execute(get_player_sql, (username,))
        tup = c.fetchone()
        if not tup:
            raise AttributeError(f"No player found with username {username}")
        idx = tup[1]
        idxs, names, mens, morales, ammos = map(lambda x: x.split(","), tup[2:])
        lst = []
        if idxs:
            lst = [ActiveUnit(name, men, morale, ammo, index) for (name, men, morale, ammo, index) in
                   zip(names, mens, morales, ammos, idxs)]
        return Player(lst, idx)


if __name__ == '__main__':
    print(get_player("Itay").to_dict())
