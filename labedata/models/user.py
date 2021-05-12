from ..db import get_db
from typing import Union, Dict

class User():

    @staticmethod
    def fetch_by_login(login) -> Union[Dict[str, str], None]:
        return db.execute(
            "SELECT * FROM users WHERE login = ?", (login,)
        ).fetchone()

    @staticmethod
    def fetch_by_user_id(user_id) -> Union[Dict[str, str], None]:
        return db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()