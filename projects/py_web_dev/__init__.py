from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash
import dash_bootstrap_components as dbc

PATH_APP = "/home/ansarimn/Downloads/tools and projects/projects/py_web_dev/"
PATH_STATIC = PATH_APP+"static/"
PATH_TEMPLATE = PATH_APP+"templates/"
IMAGE_DIR = PATH_STATIC+"image/"


app = Flask(__name__, static_folder=PATH_STATIC, template_folder=PATH_TEMPLATE)
dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config ["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config ["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy (app)


class general ():
    id0, id1 = 0, 0
    id2, id3 = 0, 0
    s0, s1 = "aa", "aa"
    s2, s3 = "aa", "aa"

    def __init__(self, id0, **kwargs):
        self.id0 = id0
        self.id1, self.id2, self.id3 = kwargs.get("id1", 0), kwargs.get("id2", 0), kwargs.get("id3", 0)
        self.s0, self.s1, self.s2, self.s3 = kwargs.get("s0"), kwargs.get("s1"), kwargs.get("s2"), kwargs.get("s3")

