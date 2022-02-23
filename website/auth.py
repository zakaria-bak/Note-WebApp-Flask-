from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password Try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user = current_user)


@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        email = request.form["email"]
        firstName = request.form["firstName"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        
        #check if the user exist or not (email)
        user = User.query.filter_by(email=email).first() 
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greter than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greter than 1 characters.', category='error')
        elif password2 != password1:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name = firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    

    return render_template("sign_up.html", user = current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

