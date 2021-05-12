import functools
from forms import LoginForm, RegisterForm
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    form=RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            login = form.login.data
            email = form.email.data
            db = get_db()
            error = None

            # server-side validation even though form has it"s own
            # to-do validate payload for flashing or logging safety
            if not username:
                error = "Username is required."
            elif not password:
                error = "Password is required."
            elif not email:
                error = "Email is required."
            elif not login:
                error = "Login is required."
            
            elif db.execute(
                "SELECT user_id FROM users WHERE login = ?", (login,)
            ).fetchone() is not None:
                error = f"Login {login} is already registered."

            if error is None:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
                return redirect(url_for("auth.login"))

            flash(error)
    
    return render_template("auth/register.html", form=form)

@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if request.method == "POST":
        login = form.login.data
        password = form.password.data
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM users WHERE login = ?", (login,)
        ).fetchone()

        if user is None:
            error = "Incorrect login."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    
    return render_template("auth/login.html", form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE user_id = ?", (user_id,)
        ).fetchone()

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view