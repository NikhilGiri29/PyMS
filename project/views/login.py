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
            
        try:
            
            user = User.query.filter_by(email=data['email']).first()
            if user and user.password== data['password']:
                auth_token = user.encode_auth_token(user.email)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return (jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist/ Incorrect Password'
                }
                return (jsonify(responseObject)), 404

        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return (jsonify(responseObject)), 500


