from model import User
from db.utils import add_single


def add_user(name: str, email: str, token: str, engine):
    add_single(User(name, email, token), engine)
