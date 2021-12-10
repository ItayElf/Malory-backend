import sqlite3
from hashlib import md5

import flask

from settings import DB_LOCATION
from string import ascii_letters, digits
from random import choice


def register_user(username: str, password: str) -> bool:
    """Registers a user to the database, returns true if successful"""
    pool = ascii_letters + digits
    salt = "".join([choice(pool) for i in range(8)])
    hashed = md5((password + salt).encode()).hexdigest()
    with sqlite3.connect(DB_LOCATION) as conn:
        try:
            conn.execute("INSERT INTO users(username, password, salt) VALUES(?, ?, ?)", (username, hashed, salt))
        except sqlite3.IntegrityError:  # username already exists
            return False
        conn.commit()
    return True


def verify_user(username: str, password: str) -> bool:
    """Checks whether the given password is the correct password for the given username (returns False also if the user doesn't exists)"""
    with sqlite3.connect(DB_LOCATION) as conn:
        c = conn.cursor()
        c.execute("SELECT password, salt FROM users WHERE username=?", (username,))
        tup = c.fetchone()
        if not tup:
            return False
        hashed, salt = tup
        return md5((password + salt).encode()).hexdigest() == hashed


def get_user_idx(username: str) -> int:
    """Returns the user id which correspond to the given username"""
    with sqlite3.connect(DB_LOCATION) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=?", (username,))
        tup = c.fetchone()
        if not tup:
            raise AttributeError(f"No player named {username} was found.")
        return tup[0]


def get_user_name(idx: int) -> str:
    """Returns the username which correspond to the given index"""
    with sqlite3.connect(DB_LOCATION) as conn:
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE id=?", (idx,))
        tup = c.fetchone()
        if not tup:
            raise AttributeError(f"No player with index {idx} was found.")
        return tup[0]
