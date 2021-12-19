import sqlite3
from typing import List

from malory.classes.room import Room
from malory.orm.active_unit_orm import get_player
from malory.orm.user_orm import get_user_name
from settings import DB_LOCATION


def get_available_rooms() -> List[Room]:
    """Returns all rooms that can be joined to"""
    with sqlite3.connect(DB_LOCATION) as conn:
        c = conn.cursor()
        c.execute("SELECT name, points, player1_id FROM rooms WHERE player2_id IS NULL")
        lst = c.fetchall()
        return [Room(name, points, get_player(get_user_name(idx))) for (name, points, idx) in lst]


def get_room(room_name: str) -> Room:
    """Returns a room by name, throwing AttributeError if not found"""
    with sqlite3.connect(DB_LOCATION) as conn:
        c = conn.cursor()
        c.execute("SELECT name, points, player1_id, player2_id FROM rooms WHERE name = ?", (room_name,))
        tup = c.fetchone()
        if not tup:
            raise AttributeError(f"Room {room_name} was not found")
        name, points, player1_id, player2_id = tup
        player1 = get_player(get_user_name(player1_id))
        player2 = None if player2_id is None else get_player(get_user_name(player2_id))
        return Room(name, points, player1, player2)


def join_room(room_name: str, idx: int) -> None:
    """Adds a player to a room, throwing AttributeError if room is full or not found"""
    with sqlite3.connect(DB_LOCATION) as conn:
        username = get_user_name(idx)
        room = get_room(room_name)
        if not not room.player2:
            raise AttributeError("Room is full")
        if room.player1.idx == idx:
            raise AttributeError(f"Player {username} is already in room {room.name}")
        conn.execute("UPDATE rooms SET player2_id=? WHERE name=?", (idx, room_name))
        conn.commit()


def create_room(room_name: str, points: int, idx: int) -> None:
    """Creates a room in the database"""
    with sqlite3.connect(DB_LOCATION) as conn:
        get_user_name(idx)
        try:
            conn.execute("INSERT INTO rooms(name, points, player1_id) VALUES(?,?,?)", (room_name, points, idx))
            conn.commit()
        except sqlite3.IntegrityError:
            raise AttributeError(f"Room name {room_name} is already taken")


def leave_room(room_name: str, idx: int) -> None:
    """Removes a player from a room, throwing AttributeError if not in room"""
    with sqlite3.connect(DB_LOCATION) as conn:
        username = get_user_name(idx)
        room = get_room(room_name)
        if room.player1.idx == idx:
            conn.execute("DELETE FROM rooms WHERE name=?", (room_name,))
            conn.commit()
            if room.player2:
                create_room(room.name, room.points, room.player2.idx)
        elif room.player2 and room.player2.idx == idx:
            conn.execute("UPDATE rooms SET player2_id=NULL WHERE name=?", (room_name,))
            conn.commit()
        else:
            raise AttributeError(f"Player {username} is not in room named {room.name}")
