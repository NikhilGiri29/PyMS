# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import datetime
import jwt
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Enum
import enum

from project.models.init_db import db


class Film(db.Model):
    """Example model"""
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    pub_date = Column(Date, default=datetime.datetime.now)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    cast = db.relationship("Actor", secondary="film_cast")


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    films = db.relationship("Film", secondary="film_cast")


class FilmCast(db.Model):
    __tablename__ = "film_cast"

    film_id = Column(
        Integer, ForeignKey(Film.id, ondelete="CASCADE"), primary_key=True
    )
    actor_id = Column(
        Integer,
        ForeignKey(Actor.id, ondelete="CASCADE"),
        key="id",
        primary_key=True,
    )
    actor = db.relationship(Actor)
    film = db.relationship(Film)

###################################################################

class typeOfUser(enum.Enum):
    customer = "customer"
    restaurant = "restaurant"
    delivery = "delivery"

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.Integer, unique = True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.column(db.Enum(typeOfUser),nullable = False)
    registered_on = db.Column(db.DateTime, default=datetime.datetime.now,nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self,name,address,contact,email,password,user_type,admin) :
        self.name = name 
        self.address = address 
        self.contact =  contact 
        self.email =  email 
        self.password = password 
        self.user_type = user_type 
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self,email):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': email
            }
            return jwt.encode(
                payload,
                'test',
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, 'test')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
