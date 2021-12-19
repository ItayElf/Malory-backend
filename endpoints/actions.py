import json
from typing import Tuple

import flask
from flask import request
from main import app
from malory.orm.active_unit_orm import add_active_unit, active_unit_owner, delete_active_unit
from malory.orm.room_orm import get_room, join_room, create_room, leave_room
from malory.orm.user_orm import register_user, verify_user, get_user_idx


def handle_auth(req: flask.Request) -> Tuple[str, int]:
    """Tests if the username and password given are correct"""
    if "username" not in req.form or "password" not in req.form:
        return "Missing username or password in form", 400
    username = req.form.get("username")
    password = req.form.get("password")
    try:
        verify_user(username, password)
    except ValueError:
        return "Invalid user credentials", 401
    return "", 200


# --- USERS ---
@app.route("/action/register", methods=["POST"])
def register_action():
    if "username" not in request.form or "password" not in request.form:
        return "Missing username or password in form", 400
    username = request.form.get("username")
    password = request.form.get("password")
    try:
        return json.dumps(register_user(username, password))
    except ValueError as e:
        return str(e), 406


# --- ACTIVE UNITS ---
@app.route("/action/add_unit", methods=["POST"])
def add_unit_action():
    tup = handle_auth(request)
    if tup[0]:
        return tup
    username = request.form.get("username")
    if "unit_name" not in request.form:
        return "Missing unit_name in form", 400
    unit_name = request.form.get("unit_name")
    try:
        player_id = get_user_idx(username)
        res = add_active_unit(unit_name, player_id)
        return json.dumps(res)
    except AttributeError as e:
        return str(e), 404


@app.route("/action/remove_unit", methods=["DELETE"])
def remove_unit_action():
    tup = handle_auth(request)
    if tup[0]:
        return tup
    username = request.form.get("username")
    if "unit_idx" not in request.form or not request.form.get("unit_idx").isdigit():
        return "Missing unit_idx in form or it is not a valid one", 400
    unit_idx = int(request.form.get("unit_idx"))
    if get_user_idx(username) != active_unit_owner(unit_idx):
        return "Cannot remove unit of another player", 401
    return json.dumps(delete_active_unit(unit_idx))


# --- ROOMS ---
@app.route("/action/join_room", methods=["POST"])
def join_room_action():
    tup = handle_auth(request)
    if tup[0]:
        return tup
    if "room_name" not in request.form:
        return "Missing room_name from form", 400
    try:
        room = get_room(request.form.get("room_name"))
        join_room(room.name, get_user_idx(request.form.get("username")))
        return "", 200
    except AttributeError as e:
        return str(e), 404


@app.route("/action/create_room", methods=["POST"])
def create_room_action():
    tup = handle_auth(request)
    if tup[0]:
        return tup
    if "room_name" not in request.form:
        return "Missing room_name from form", 400
    if "points" not in request.form or not request.form.get("points", type=int):
        return "Missing points in form or it is not a valid one", 400
    points = request.form.get("points", type=int)
    room_name = request.form.get("room_name")
    username = request.form.get("username")
    try:
        create_room(room_name, points, get_user_idx(username))
        return "", 200
    except AttributeError as e:
        return str(e), 403


@app.route("/action/leave_room", methods=["POST"])
def leave_room_action():
    tup = handle_auth(request)
    if tup[0]:
        return tup
    if "room_name" not in request.form:
        return "Missing room_name from form", 400
    room_name = request.form.get("room_name")
    username = request.form.get("username")
    try:
        leave_room(room_name, get_user_idx(username))
        return "", 200
    except AttributeError as e:
        return str(e), 404
