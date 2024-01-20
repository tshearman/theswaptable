from sqlmodel import and_

from backend.sqldb import utils
from backend.sqldb.model import Item, User, Vote


@utils.all_(Item)
def read_user_library(*, user: User):
    return and_(Item.owner_id == user.id)


@utils.all_(Vote)
def read_user_votes(*, user: User):
    return Vote.user_id == user.id
