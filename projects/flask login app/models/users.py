import sys
# sys.path.append("../")
from __init__ import db
from flask_login import UserMixin
from sqlalchemy import func


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, db.Sequence('User_id_seq'), primary_key=True)

    # username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password2 = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(120))
    date = db.Column(db.TIMESTAMP(timezone=True), default=func.now())
    notes = db.relationship ("Note")


    #created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    #updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)