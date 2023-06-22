from pydantic import EmailStr
from backend.model import User
from backend.db.utils import add_single


def add_user(name: str, email: EmailStr, token: str, engine):
    add_single(User(name, email, token), engine)
