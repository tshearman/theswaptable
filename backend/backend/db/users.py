from pydantic import UUID4, EmailStr
from sqlmodel import select
from backend.model import User
from backend.db.utils import add_single


def add_user(name: str, email: EmailStr, token: str, session):
    add_single(User(name=name, email=email, token=token), session)


def lookup_user(id: UUID4, session) -> User | None:
    return session.exec(select(User).where(User.id == id)).first()


def lookup_user_by_email(email: EmailStr, session) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()


def count_users(session):
    return session.query(select(User.id).distinct().subquery()).count()
