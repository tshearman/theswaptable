from pydantic import UUID4, EmailStr
from backend.model import User
from backend.sqldb import utils
from sqlmodel import Session, true


@utils.all(User)
def read_all():
    return true


@utils.first(User)
def read(*, id: UUID4):
    return User.id == id


@utils.first(User)
def read_by_email(*, email: EmailStr):
    return User.email == email


def delete(session: Session, *, id: UUID4) -> User:
    user = read(session, id=id)
    session.delete(user)
    session.commit()
    return user


@utils.count(User)
def count_all():
    return true


def create(session: Session, *, user: User) -> User:
    return utils.create(User)(session, user)
