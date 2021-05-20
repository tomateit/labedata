from werkzeug.security import check_password_hash, generate_password_hash
from ..db import get_db
from typing import Union, Dict, Tuple, Optional
from uuid import uuid4

class User():

    @staticmethod
    def fetch_by_login(login) -> Optional[Dict[str, str]]:
        db = get_db()
        return db.execute(
            "SELECT * FROM users WHERE login = ?", (login,)
        ).fetchone()

    @staticmethod
    def fetch_by_user_id(user_id) -> Optional[Dict[str, str]]:
        db = get_db()
        return db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()

    @staticmethod
    def register_new_user(username=None, password=None, login=None, email=None, **kwargs) -> Optional[str]:
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
        elif User.fetch_by_login(login) is not None:
            error = f"Login {login} is already registered."
        else:
            user_id = str(uuid4())
            db = get_db()
            db.execute("INSERT INTO users (user_id, login, username, email, password) VALUES (?, ?, ?, ?, ?)",
                        (user_id, login, username, email, generate_password_hash(password))
            )
            db.commit()
        return error

    @staticmethod
    def authenticate(login: str=None, password: str=None)-> Tuple[Optional[Dict[str,str]], Optional[str]]:
        error = None
        if not login:
            return None, "Login not provided"
        if not password:
            return None, "Password not provided"
        
        user = User.fetch_by_login(login)
        if not user:
            return None, "No such user"
        if not check_password_hash(user["password"], password):
            return None, "Password is incorrect"

        return user, None