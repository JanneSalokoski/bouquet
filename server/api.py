from flask import (
    Blueprint, flash, g, request, jsonify
)

from werkzeug.exceptions import abort

from server.auth import login_required
from server.db import get_db

import json

bp = Blueprint("api", __name__, url_prefix="/api")

# Users

@bp.route("/users")
def users():
    db = get_db()
    users = db.execute(
        "SELECT * FROM users"
    ).fetchall()

    return [tuple(row) for row in users]

@bp.route("/user", methods=("POST",))
def add_user():
    # TODO: Implement this
    return []

@bp.route("/user/<id>", methods=("GET", "POST"))
def user(id):
    db = get_db()
    if request.method == "GET":
        user = db.execute(
            "SELECT * FROM users WHERE id=?", 
            (id,)
        ).fetchone()

        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
        }

    elif request.method == "POST":
        # TODO:implement
        pass

    return []

# Quests

class Quest:
    def __init__(self, id, name, email, diet, participating, responded, edited, group_id, group_name, type_id, type_name):
        self.id = id
        self.name = name
        self.email = email
        self.diet = diet
        self.participating = bool(participating)
        self.responded = responded
        self.edited = edited
        self.group_id = group_id
        self.group_name = group_name
        self.type_id = type_id
        self.type_name = type_name

    @classmethod
    def from_row(cls, row):
        print(type(row))
        return cls(
            row["id"],
            row["name"],
            row["email"],
            row["diet"],
            row["participating"],
            row["responded"],
            row["edited"],
            row["grp_id"],
            row["group_name"],
            row["type_id"],
            row["type_name"]
        )

    def to_json(self):
        return self.__dict__

@bp.route("/quests")
def quests():
    db = get_db()

    quests = []

    group_id = request.args.get("group")

    if group_id is None:
        quests = db.execute(
            """SELECT q.id, q.name, q.email, q.diet, q.participating,
            q.responded, q.edited, q.grp_id, g.name as 'group_name',
            q.type_id, t.name as 'type_name'
            FROM quests as q
            INNER JOIN groups as g ON g.id == q.grp_id
            INNER JOIN types as t ON t.id == q.type_id
            """
        ).fetchall()

    quests = db.execute(
        """SELECT q.id, q.name, q.email, q.diet, q.participating,
        q.responded, q.edited, q.grp_id, g.name as 'group_name',
        q.type_id, t.name as 'type_name'
        FROM quests as q
        INNER JOIN groups as g ON g.id == q.grp_id
        INNER JOIN types as t ON t.id == q.type_id
        WHERE g.id == ?
        """,
        (group_id,)
    ).fetchall()

    return [Quest.from_row(row).to_json() for row in quests]

@bp.route("/quest/<id>", methods=("GET", "POST"))
def quest(id):
    db = get_db()
    if request.method == "GET":
        quest = db.execute(
            "SELECT * FROM quests WHERE id=?", 
            (id,)
        ).fetchone()

        if quest is not None:
            return Quest.from_row(quest).to_json()

        return "Quest not found"

    elif request.method == "POST":
        # TODO:implement
        pass

# Groups

class Group:
    def __init__(self, id, name, passkey):
        self.id = id
        self.name = name
        self.passkey = passkey

    @classmethod
    def from_row(cls, row):
        print(type(row))
        return cls(row["id"], row["name"], row["passkey"])

@bp.route("/groups")
def groups():
    db = get_db()

    groups = db.execute(
        "SELECT * FROM groups"
    ).fetchall()

    return [Group.from_row(row) for row in groups]

 
@bp.route("/group/<id>", methods=("GET", "POST"))
def group(id):
    db = get_db()
    if request.method == "GET":
        group = db.execute(
            "SELECT * FROM groups WHERE id=?", 
            (id,)
        ).fetchone()

        if group is not None:
            return Group.from_row(group)

        return "Quest not found"

    elif request.method == "POST":
        # TODO:implement
        pass

    return []

# Types



# Sessions


