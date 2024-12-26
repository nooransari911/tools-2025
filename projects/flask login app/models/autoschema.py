from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import Schema, EXCLUDE, fields, post_load
from .users import User
from .notes import Note

class UserSchema (SQLAlchemyAutoSchema):
    class Meta:
        model = User
        unknown = EXCLUDE
        include_relationships = True
        load_instance = True


class NoteSchema (SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        unknown = EXCLUDE
        include_relationships = True
        load_instance = True