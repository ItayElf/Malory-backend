import json
from flask import abort
from main import app
from malory.orm.attribute_orm import get_all_attributes, get_attribute
from malory.orm.unit_orm import get_all_units, get_unit
from settings import VERSION


# --- SETTINGS ---
@app.route("/api/version/")
def version_api():
    return VERSION


# --- ATTRIBUTES ---
@app.route("/api/attributes/")
def attributes_api():
    attrs = [a.to_dict() for a in get_all_attributes()]
    return json.dumps(attrs, indent=4)


@app.route("/api/attribute/<attr_name>/")
def attribute_api(attr_name):
    try:
        attr = get_attribute(attr_name.title())
        return json.dumps(attr.to_dict(), indent=4)
    except AttributeError:
        abort(404)


# --- UNITS ---
@app.route("/api/units/")
def units_api():
    units = [u.to_dict() for u in get_all_units()]
    return json.dumps(units, indent=4)


@app.route("/api/unit/<unit_name>/")
def unit_api(unit_name):
    try:
        unit = get_unit(unit_name.title())
        return json.dumps(unit.to_dict(), indent=4)
    except AttributeError:
        abort(404)
