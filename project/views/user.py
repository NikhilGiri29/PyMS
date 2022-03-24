# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals
from typing import Tuple
from datetime import datetime

import connexion
from flask import jsonify

from project.models.init_db import db
from project.models.models import User
from project.serializers.serializers import UserSchema


def get() -> Tuple[dict, int]:
    query = User.query.paginate(
        connexion.request.args.get("paginationKey", 1),
        connexion.request.args.get("pageSize", 5)
    )
    schema = UserSchema()
    result = schema.dump(query.items, many=True)
    return jsonify(result), 200


def search() -> Tuple[dict, int]:
    return get()


def post() -> dict:
    if connexion.request.is_json:
        data = connexion.request.get_json()
        actor = User(name=data["name"], address=data["address"],contact=data['contact'],email = data["email"], password=data['password'],user_type = data["user_type"],registered_on=datetime.strptime(data["pubDate"], "%Y-%m-%d").date(), admin = data['admin'])
        db.session.commit()

        return jsonify(UserSchema().dump(actor))
    return jsonify({})

