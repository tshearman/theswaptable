from backend.db.items import lookup_item
from backend.db.voting import users_votes_query, active_votes_query
from pydantic import UUID4
from sqlmodel import select, Session
from backend.model import Item, User


def user_voted_items(user_id: UUID4, session: Session) -> list[(Item, User)]:
    user_votes = users_votes_query(user_id, session)
    return session.exec(
        select(Item, User)
        .join(User)
        .join(user_votes, onclause=Item.id == user_votes.c.item_id)
    ).all()


def count_votes(item_id: UUID4, session: Session) -> int | None:
    if lookup_item(item_id, session) is None:
        return None
    active_votes_ = active_votes_query(session)
    return session.query(
        select(active_votes_).where(active_votes_.c.item_id == item_id).subquery()
    ).count()
