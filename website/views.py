from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import  Note
from . import db

#creating a views bluprint
views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        note = request.form['note']

        if len(note) < 1:
            flash('note too short!', category='error')
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template('home.html', user=current_user)

@views.route('/delete/<int:id>')
def delete(id):
    note_to_delete = Note.query.get(int(id))

    if note_to_delete:
       db.session.delete(note_to_delete)
       db.session.commit()
       return redirect('/')
