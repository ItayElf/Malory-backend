import sqlite3
from typing import List

from malory.classes.unit import Unit
from malory.classes.attribute import Attribute

get_unit_sql = """
SELECT group_concat(a.name),group_concat(a.description),group_concat(a.id), u.* 
FROM units u
LEFT JOIN unit_attrs ua ON ua.unit_id=u.id
LEFT JOIN attrs a ON a.id=ua.attr_id
WHERE u.name=?
GROUP BY u.name
"""


def get_unit(name: str) -> Unit:
    """Returns a unit based on a name, raises an AttributeError if there is no matching unit"""
    with sqlite3.connect("malory.db") as conn:
        c = conn.cursor()
        c.execute(get_unit_sql, (name,))
        tup = c.fetchone()
        if not tup:
            raise AttributeError(f"No unit named {name}")
        names, descs, idxs = tup[:3]
        lst = [Attribute(name, desc, idx) for name, desc, idx in
               zip(names.split(","), descs.split(","), idxs.split(","))]
        data = list(tup[4:]) + [lst, tup[3]]
    return Unit(*data)


def get_all_units() -> List[Unit]:
    """Returns a list of all units"""
    query = get_unit_sql.replace("WHERE u.name=?", "")
    res = []
    with sqlite3.connect("malory.db") as conn:
        c = conn.cursor()
        c.execute(query)
        fetched = c.fetchall()
        for tup in fetched:
            names, descs, idxs = tup[:3]
            lst = []
            if names:
                lst = [Attribute(name, desc, idx) for name, desc, idx in
                       zip(names.split(","), descs.split(","), idxs.split(","))]
            data = list(tup[4:]) + [lst, tup[3]]
            res.append(Unit(*data))
    return res
