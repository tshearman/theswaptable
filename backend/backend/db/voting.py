from backend.model import Vote
from backend.db.utils import add_single
from sqlmodel import Session, select, func, and_
from pydantic import UUID4


def vote(vote: Vote, session: Session):
    return add_single(vote, session)


def unvote(vote: Vote, session: Session):
    vote_updated = Vote(item_id=vote.item_id, user_id=vote.user_id, is_active=False)
    return add_single(vote_updated, session)


def active_votes_query(session: Session):
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


def active_votes(session: Session) -> list[Vote]:
    results = session.query(active_votes_query(session)).all()
    return list(map(Vote.from_tuple, results))


def users_votes_query(user_id: UUID4, session: Session):
    active_votes_ = active_votes_query(session)
    return select(active_votes_).where(active_votes_.c.user_id == user_id).subquery()


def users_votes(user_id: UUID4, session: Session) -> list[Vote]:
    results = session.query(users_votes_query(user_id, session)).all()
    return list(map(Vote.from_tuple, results))
