from sqlmodel import and_
from backend.model import Item, User, Vote
from backend.db import utils


@utils.all(Item)
def read_user_library(*, user: User):
    return and_(Item.owner_id == user.id)


@utils.all(Vote)
def read_user_votes(*, user: User):
    return Vote.user_id == user.id
