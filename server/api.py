from flask import (
    Blueprint, flash, g, request, jsonify
)

from werkzeug.exceptions import abort

from server.auth import login_required
from server.db import get_db

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/users")
def users():
    db = get_db()
    users = db.execute(
        "SELECT * FROM users"
    ).fetchall()

    return [tuple(row) for row in users]
