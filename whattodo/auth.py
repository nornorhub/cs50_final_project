# Authentication actions


# Imports
import functools

from whattodo.db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


# Sets the view blueprint variable
bp = Blueprint("auth", __name__, url_prefix="/auth")


# View for registering users
@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        # Validates user input
        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif db.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone() is not None:
            error = "Username {} is already taken".format(username)

        # Stores user info into the database
        if error is None:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)", 
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        
        # Send the error in a flash message
        flash(error)

    # Returns the register view in case of a GET request or
    # An input validation error
    return render_template("auth/register.html")


# View for logging in users
@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        passowrd = request.form["password"]
        db = get_db()
        error = None

        # Queries the database for user info
        # Returns 'None' if not registered
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        # Validates user input
        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], passowrd):
            error = "Incorrect password"
        
        # Stores user id in session and
        # Redirects him to 'index.html'
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for('index.index'))

        # Send the error in a flash message
        flash(error)


    # Returns the register view in case of a GET request or
    # An input validation error
    return render_template("auth/login.html")


# Loads logged in user
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    db = get_db()

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()


# Logs out user by clearing the session and
# Redirects user to 'login.html'
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# Requires the user to be logged in to access a certain view
# Redirects user to 'login.html' if not logged in
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)

    return wrapped_view