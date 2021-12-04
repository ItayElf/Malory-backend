import sqlite3
from typing import List

from malory.classes.attribute import Attribute


def get_attribute(name: str) -> Attribute:
    """Returns an attribute based on a name, raising an AttributeError if there is no matching attribute"""
    with sqlite3.connect("malory.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM attrs WHERE name=?", (name,))
        tup = c.fetchone()
        if not tup:
            raise AttributeError(f"No attribute named {name}.")
        idx, name, desc = tup
    return Attribute(name, desc, idx)


def get_all_attributes() -> List[Attribute]:
    """Returns a list of all attributes"""
    with sqlite3.connect("malory.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM attrs")
        lst = c.fetchall()
    return [Attribute(name, desc, idx) for (idx, name, desc) in lst]
