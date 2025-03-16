from flask import Flask, Blueprint
from views import views
from auth import auth
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
#db = SQLAlchemy ()
DB_NAME = "database.db"
DB_URI = f"sqlite:///{DB_NAME}"



#def create_app ():
app = Flask (__name__)
app.config ["SECRET_KEY"] = "ABCDXX"
app.config ["SQLALCHEMY_DATABASE_URI"] = DB_URI

app.register_blueprint (views, url_prefix="/")
app.register_blueprint (auth, url_prefix="/auth/")
db = SQLAlchemy ()
db.init_app(app)

from models.users import User
from models.notes import Note


login_manager = LoginManager ()
login_manager.login_view = "auth.auth_login_get"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))




with app.app_context():
    db.drop_all ()
    db.create_all ()
    session = db.session