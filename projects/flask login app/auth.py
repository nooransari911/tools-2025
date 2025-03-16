from flask import Blueprint, render_template, request, flash, redirect, url_for
#from main import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint ("auth", __name__)


#from models.autoschema import UserSchema, NoteSchema

# add parameter in render_template: user=current_user;
# refer this parameter in template to access logged in user;




@auth.route ("/")
def auth_root ():
    return "<h1>auth root</h1>"

@auth.route ("/login", methods=["GET"])
def auth_login_get ():
    return render_template ("login.html")



@auth.route ("/login", methods=["POST"])
def auth_login_post ():
    email = request.form.get("email")
    password = request.form.get("password")

    from models.users import User
    from __init__ import session
    user = User.query.filter_by(email=email).first()

    if user:
        if check_password_hash(user.password2, password):
            flash("Login success", category="success")
            login_user (user, remember=True)
            return redirect(url_for("views.views_root"))
        else:
            flash("Wrong password. Try again", category="error")
    else:
        flash("Wrong email or email does not exist. Try again", category="error")


    return render_template ("login.html")






@auth.route ("/signup", methods=["GET"])
def auth_signup_get ():
    return render_template ("signup.html")


@auth.route("/signup", methods=["POST"])
def auth_signup_post ():
    email = request.form.get ("email")
    firstName = request.form.get ("firstName")
    password1 = request.form.get ("password1")
    password2 = request.form.get ("password2")

    if (password1 != password2):
        flash("Passwords don't match", category="error")
        return render_template("signup.html")


    #print (request.form)

    from models.autoschema import UserSchema, NoteSchema
    from models.users import User
    from models.notes import Note
    from __init__ import session

    user = User.query.filter_by(email=email).first()
    if user:
        flash ("Email already exists. Try again", category="error")
        return render_template("signup.html")


    user_signup = User (
        email=email,
        first_name=firstName,
        password2=generate_password_hash(password2)
    )

    #user_signup = UserSchema().load (request.form, session=session)
    #print(user_signup)
    session.add(user_signup)
    session.commit()

    print (UserSchema().dump (obj=User.query.all(), many=True))
    flash ("Signup success", category="success")
    login_user(user_signup, remember=True)

    return redirect (url_for("views.views_root"))




@auth.route ("/logout")
@login_required
def auth_logout ():
    logout_user()
    return redirect(url_for("auth.auth_login_get"))