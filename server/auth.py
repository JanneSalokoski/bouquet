import functools

from flask import (
    Blueprint, flash, g, redirect, request, session
)

from werkzeug.security import check_password_hash, generate_password_hash

from server.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()


@bp.route("/login", methods=("POST",))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], password):
            print(password)
            print(user["password"])
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]

            return "Ok."

        flash(error)
        return error

@bp.route("/logout", methods=("POST",))
def logout():
    session.clear()
    return "Ok."

def login_required(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.user is None:
            return "No good"

        return view(**kwargs)

    return wrapped
