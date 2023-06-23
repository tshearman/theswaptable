from backend.model import Vote
from backend.db.utils import add_single
from sqlmodel import select, func, and_
from pydantic import UUID4


def update_vote(item_id: UUID4, user_id: UUID4, session, is_active=True):
    return add_single(
        Vote(item_id=item_id, user_id=user_id, is_active=is_active), session
    )


def vote_for(item_id: UUID4, user_id: UUID4, session):
    return update_vote(item_id, user_id, session)


def remove_vote_for(item_id: UUID4, user_id: UUID4, session):
    return update_vote(item_id, user_id, session, is_active=False)


def active_votes_query(session):
    rank = (
        func.rank()
        .over(
            order_by=[Vote.create_ts.desc(), func.random()],
            partition_by=[Vote.item_id, Vote.user_id],
        )
        .label("rnk")
    )
    inner = session.query(Vote, rank).subquery()
    return (
        select(
            [
                inner.c.item_id,
                inner.c.user_id,
                inner.c.is_active,
                inner.c.id,
                inner.c.create_ts,
            ]
        )
        .where(and_(inner.c.rnk == 1, inner.c.is_active))
        .subquery()
    )


def active_votes(session) -> list[Vote]:
    results = session.query(active_votes_query(session)).all()
    return list(map(Vote.from_tuple, results))


def users_votes_query(user_id: UUID4, session):
    active_votes_ = active_votes_query(session)
    return select(active_votes_).where(active_votes_.c.user_id == user_id).subquery()


def users_votes(user_id: UUID4, session) -> list[Vote]:
    results = session.query(users_votes_query(user_id, session)).all()
    return list(map(Vote.from_tuple, results))


def count_votes(item_id: UUID4, session):
    active_votes_ = active_votes_query(session)
    return session.query(
        select(active_votes_).where(active_votes_.c.item_id == item_id).subquery()
    ).count()
