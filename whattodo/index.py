from flask import (
    Blueprint, flash, render_template, request, json, session
)
from whattodo.auth import login_required
from whattodo.db import get_db

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    db = get_db()

    if request.method == "POST":

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
                'UPDATE lists SET list = ?', 
                (json.dumps(request.json),)
            )

        db.commit()

        return "List saved."

    if db.execute(
            'SELECT list FROM lists WHERE owner_id = ?', 
            (session['user_id'],)
        ).fetchone() != None:
        

        todoList = db.execute(
            'SELECT list FROM lists WHERE owner_id = ?',
            (session["user_id"],)
        ).fetchone()[0]

        return render_template('index/index.html', todoList=json.loads(todoList))

    return render_template('index/index.html')
