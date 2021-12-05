import json
from flask import abort, request
from main import app
from malory.orm.user_orm import register_user


@app.route("/action/register", methods=["POST"])
def register_action():
    if "username" not in request.form or "password" not in request.form:
        abort(400)
    username = request.form.get("username")
    password = request.form.get("password")
    return json.dumps(register_user(username, password))

