from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

#creating an auth bluprint
auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first() 
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfuly!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template('login.html', user=current_user)

@auth.route("/sign-up", methods=["GET", "POST"])
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
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('account created!!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template('sign_up.html', user=current_user)

@auth.route("logout")
@login_required # we should be login before we logout
def logout():
    logout_user()
    return  redirect(url_for('auth.login'))





