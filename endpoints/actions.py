import json
from flask import abort, request
from main import app
from malory.orm.active_unit_orm import add_active_unit, active_unit_owner, delete_active_unit
from malory.orm.user_orm import register_user, verify_user, get_user_idx


@app.route("/action/register", methods=["POST"])
def register_action():
    if "username" not in request.form or "password" not in request.form:
        abort(400)
    username = request.form.get("username")
    password = request.form.get("password")
    return json.dumps(register_user(username, password))


@app.route("/action/add_unit", methods=["POST"])
def add_unit_action():
    if "username" not in request.form or "password" not in request.form:
        abort(400)
    username = request.form.get("username")
    password = request.form.get("password")
    if not verify_user(username, password):
        abort(401)
    if "unit_name" not in request.form:
        abort(400)
    unit_name = request.form.get("unit_name")
    try:
        player_id = get_user_idx(username)
        res = add_active_unit(unit_name, player_id)
        return json.dumps(res)
    except AttributeError:
        abort(404)


@app.route("/action/remove_unit", methods=["DELETE"])
def remove_unit_action():
    if "username" not in request.form or "password" not in request.form:
        abort(400)
    username = request.form.get("username")
    password = request.form.get("password")
    if not verify_user(username, password):
        abort(401)
    if "unit_idx" not in request.form or not request.form.get("unit_idx").isdigit():
        abort(400)
    unit_idx = int(request.form.get("unit_idx"))
    if get_user_idx(username) != active_unit_owner(unit_idx):
        abort(401)
    return json.dumps(delete_active_unit(unit_idx))




