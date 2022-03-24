from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema

from project.models.models import Film, Actor, User


class ActorSchema(SQLAlchemySchema):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'surname')


class FilmSchema(SQLAlchemySchema):
    cast = fields.Nested(ActorSchema, many=True)
    pubDate = fields.String(required=True, data_key='pub_date', attribute="pub_date")

    class Meta:
        model = Film
        fields = ('id', 'name', 'pub_date', 'cast')

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        fields = ('id', 'name', 'address', 'contact','email','password','user_type','registered_on','admin')