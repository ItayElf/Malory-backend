import json
from flask import request
from main import app
from malory.orm.active_unit_orm import get_active_unit, get_player
from malory.orm.attribute_orm import get_all_attributes, get_attribute
from malory.orm.unit_orm import get_all_units, get_unit
from malory.orm.user_orm import verify_user
from settings import VERSION


# --- SETTINGS ---
@app.route("/api/version")
def version_api():
    return VERSION


# --- ATTRIBUTES ---
@app.route("/api/attributes")
def attributes_api():
    attrs = [a.to_dict() for a in get_all_attributes()]
    return json.dumps(attrs, indent=4)


@app.route("/api/attribute/<attr_name>")
def attribute_api(attr_name):
    try:
        attr = get_attribute(attr_name.title())
        return json.dumps(attr.to_dict(), indent=4)
    except AttributeError as e:
        return str(e), 404


@app.route("/api/has_attribute/<attr_name>")
def has_attribute_api(attr_name):
    full = False
    if "full" in request.args:
        full = request.args.get("full") == "true"
    units = get_all_units()
    return json.dumps([(unit.name if not full else unit.to_dict()) for unit in units if unit.has_attribute(attr_name)],
                      indent=4)


# --- UNITS ---
@app.route("/api/units")
def units_api():
    units = [u.to_dict() for u in get_all_units()]
    return json.dumps(units, indent=4)


@app.route("/api/unit/<unit_name>")
def unit_api(unit_name):
    try:
        unit = get_unit(unit_name.title())
        return json.dumps(unit.to_dict(), indent=4)
    except AttributeError as e:
        return str(e), 404


@app.route("/api/categories")
def categories_api():
    playable = True
    if "playable" in request.args:
        playable = request.args.get("playable") != "false"
    categories = list({u.category for u in get_all_units()})
    if playable:
        categories.remove("Special")
    return json.dumps(categories, indent=4)


@app.route("/api/nations")
def nations_api():
    ignore = ["Medium", "Heavy", "Light", "Special"]
    nations = list({u.category for u in get_all_units() if all([s not in u.category for s in ignore])})
    return json.dumps(nations, indent=4)


# --- ACTIVE UNITS ---

@app.route("/api/active_unit/<idx>")
def active_unit_api(idx):
    try:
        unt = get_active_unit(int(idx))
        return json.dumps(unt.to_dict(), indent=4)
    except (AttributeError, ValueError) as e:
        return str(e), 404


@app.route("/api/player/<username>")
def get_player_api(username):
    try:
        p = get_player(username)
        return json.dumps(p.to_dict(), indent=4)
    except AttributeError as e:
        str(e), 404


# --- USERS ---
@app.route("/api/verify")
def verify_api():
    if "username" not in request.args or "password" not in request.args:
        return "Missing username or password in args", 400
    username = request.args.get("username")
    password = request.args.get("password")
    return json.dumps(verify_user(username, password))
