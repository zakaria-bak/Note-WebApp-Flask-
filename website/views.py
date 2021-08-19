from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for
from werkzeug.utils import redirect
from .models import Note, User
from flask_login import login_required, current_user
from . import db


views = Blueprint('views', __name__)

@views.route("/", methods=["POST", "GET"])
def home():
    flash('To add a Note login required', category='message')
    if request.method == 'POST':
        note = request.form["note"]

        if len(note) < 1:
            flash('Note is short!', category='error')
        else:
            new_note = Note(data = note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
        
    return render_template("home.html", user = current_user)

@views.route('/delete/<int:id>')
def delete(id):
    note_to_delete = Note.query.get(int(id))

    if note_to_delete:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    
    

@views.route("/database")
def view():
    return render_template("view_database.html", values=User.query.all())

