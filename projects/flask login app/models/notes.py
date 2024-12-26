import sys
#sys.path.append("../")
from __init__ import db
from flask_login import UserMixin
from sqlalchemy import func

class Note (db.Model):
    __tablename__ = 'Note'
    id = db.Column(db.Integer, db.Sequence('Note_id_seq'), primary_key=True)
    data = db.Column(db.String (1000))
    date = db.Column(db.TIMESTAMP(timezone=True), default=func.now())
    user_id = db.Column (db.Integer, db.ForeignKey ("User.id"))

    #updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)