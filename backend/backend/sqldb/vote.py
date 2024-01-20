from pydantic import UUID4
from sqlmodel import Session, and_

from backend.model import Vote
from backend.sqldb import utils


@utils.first(Vote)
def read(*, id: UUID4):
    return Vote.id == id


@utils.first(Vote)
def read_by_user_and_item(user_id: UUID4, item_id: UUID4):
    return and_(Vote.user_id == user_id, Vote.item_id == item_id)


@utils.count(Vote)
def count_votes_by_item_id(item_id: UUID4):
    return Vote.item_id == item_id


@utils.all(Vote)
def read_votes_by_item_id(item_id: UUID4):
    return Vote.item_id == item_id


@utils.all(Vote)
def read_votes_by_user_id(user_id: UUID4):
    return Vote.user_id == user_id


def create(session: Session, *, vote: Vote) -> Vote:
    return utils.create(Vote)(session, vote)


def delete(session: Session, *, id: UUID4) -> Vote:
    return utils.delete(Vote, read)(session, id=id)
