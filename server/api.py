from flask import (
    Blueprint, request,
)

from server.auth import login_required
from server.db import get_db

import datetime
import sqlite3

bp = Blueprint("api", __name__, url_prefix="/api")

# Users

class User:
    def __init__(
            self,
            id: int, 
            username: str, 
            email: str
            ):
        self.id: int = id
        self.username: str = username
        self.email: str = email

    @classmethod
    def from_row(cls, row: sqlite3.Row):
        return cls(
                row["id"],
                row["username"],
                row["email"]
            )

@bp.route("/users")
def users():
    db = get_db()
    users = db.execute(
        "SELECT * FROM users"
    ).fetchall()

    return [User.from_row(row) for row in users]

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

        return User.from_row(user)

    elif request.method == "POST":
        # TODO:implement
        pass

    return []

# Quests

class Quest:
    def __init__(
            self, 
            id: int, 
            name: str, 
            email: str, 
            diet: str, 
            participating: bool, 
            responded: datetime.datetime, 
            edited: datetime.datetime, 
            group_id: int, 
            group_name: str, 
            type_id: int, 
            type_name: str
            ):
        self.id: int = id
        self.name: str = name
        self.email: str = email
        self.diet: str = diet
        self.participating: bool = bool(participating)
        self.responded: datetime.datetime = responded
        self.edited: datetime.datetime = edited
        self.group_id: int = group_id
        self.group_name: str = group_name
        self.type_id: int = type_id
        self.type_name: str = type_name

    @classmethod
    def from_row(cls, row: sqlite3.Row):
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
    def __init__(self, id: int, name: str):
        self.id: int = id
        self.name: str = name

    @classmethod
    def from_row(cls, row: sqlite3.Row):
        return cls(row["id"], row["name"])

    def to_json(self):
        return self.__dict__

@bp.route("/groups")
def groups():
    db = get_db()

    groups = db.execute(
        "SELECT * FROM groups"
    ).fetchall()

    return [Group.from_row(row).to_json() for row in groups]

 
@bp.route("/group/<id>", methods=("GET", "POST"))
def group(id):
    db = get_db()
    if request.method == "GET":
        group = db.execute(
            "SELECT * FROM groups WHERE id=?", 
            (id,)
        ).fetchone()

        if group is not None:
            return Group.from_row(group).to_json()

        return "Quest not found"

    elif request.method == "POST":
        # TODO:implement
        pass

    return []

# Types

class Type:
    def __init__(self, id: int, name: str):
        self.id: int = id
        self.name: str = name

    @classmethod
    def from_row(cls, row: sqlite3.Row):
        return cls(row["id"], row["name"])

    def to_json(self):
        return self.__dict__

@bp.route("/types")
def types():
    db = get_db()

    types = db.execute(
        "SELECT * FROM types"
    ).fetchall()

    return [Type.from_row(row).to_json() for row in types]

 
@bp.route("/type/<id>", methods=("GET", "POST"))
def type(id):
    db = get_db()
    if request.method == "GET":
        type = db.execute(
            "SELECT * FROM types WHERE id=?", 
            (id,)
        ).fetchone()

        if type is not None:
            return Type.from_row(type).to_json()

        return "Type not found"

    elif request.method == "POST":
        # TODO:implement
        pass

    return []
