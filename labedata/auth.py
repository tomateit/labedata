"""
Authentication functionality for the app
Provides user registration, authentication and authorization
"""
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .forms import LoginForm, RegisterForm
from .models.user import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    """
    Create new user
    """
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            error = User.register_new_user(
                login=form.login.data,
                username=form.username.data,
                password=form.password.data,
                email=form.email.data
                )
            if error is None:
                return redirect(url_for("auth.login"))

            flash(error)

    return render_template("auth/register.html", form=form)

@bp.route("/login", methods=("GET", "POST"))
def login():
    """
    Authenticate existing user
    """
    form = LoginForm()
    if request.method == "POST":
        login = form.login.data
        password = form.password.data
        user, error = User.authenticate(login, password)

        if error is None:
            session.clear()
            session["user_id"] = user["user_id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html", form=form)

# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get("user_id")
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = User.fetch_by_user_id(user_id)

@bp.route("/logout")
def logout():
    """
    Clear user's session
    """
    session.clear()
    return redirect(url_for("index"))

def login_required(view):
    """
    Middleware to check if user is authorized
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view
