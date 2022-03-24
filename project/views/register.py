# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals
from typing import Tuple
from datetime import datetime

import connexion
from flask import jsonify

from project.models.init_db import db
from project.models.models import User
from project.serializers.serializers import UserSchema


def post() -> dict:
    if connexion.request.is_json:
        data = connexion.request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            try:
                user = User(
                    name=data["name"],
                    address=data["address"],
                    contact=data['contact'],
                    email = data["email"],
                    password=data['password'],
                    user_type = data["user_type"],
                    registered_on=datetime.strptime(data["registered_on"], "%Y-%m-%d").date,
                    admin = data['admin']
                )
                
                db.session.add(user)
                db.session.commit()

                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return (jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return (jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return (jsonify(responseObject)), 202


