# Handles actions on index view
# Shows users their lists



# Imports
from flask import (
    Blueprint, flash, render_template, request, json, session
)
from whattodo.auth import login_required
from whattodo.db import get_db


# Sets the view blueprint variable
bp = Blueprint('index', __name__)


# Index view
@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    db = get_db()

    if request.method == "POST":

        # Saves the user's list
        if db.execute(
            'SELECT list FROM lists WHERE owner_id = ?', 
            (session['user_id'],)
        ).fetchone() == None:

            db.execute(
                'INSERT INTO lists (owner_id, list) VALUES (?, ?)', 
                (session['user_id'], json.dumps(request.json))
            )

        else:
            db.execute(
                'UPDATE lists SET list = ? WHERE owner_id = ?', 
                (json.dumps(request.json), session["user_id"])
            )

        db.commit()

        return "List saved."

    # Shows the user their To-Do list if they have one saved
    if db.execute(
            'SELECT list FROM lists WHERE owner_id = ?', 
            (session['user_id'],)
        ).fetchone() != None:
        

        todoList = db.execute(
            'SELECT list FROM lists WHERE owner_id = ?',
            (session["user_id"],)
        ).fetchone()[0]

        return render_template('index/index.html', todoList=json.loads(todoList))

    # Returns 'index.html' template without To-Do list for first time users
    return render_template('index/index.html')
