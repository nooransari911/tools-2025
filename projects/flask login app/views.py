from flask import Blueprint, render_template, request
#from main import app
from flask_login import login_required, current_user

views = Blueprint ("views", __name__)


@views.route ("/")
@login_required
def views_root ():
    return render_template ("home.html")
    #return "<h1>views root</h1>"

