from model import Vote
from db.utils import add_single
from sqlmodel import select, func, and_, Session
from pydantic import UUID4


def update_vote(item_id: UUID4, user_id: UUID4, engine, is_active=True):
    return add_single(
        Vote(item_id=item_id, user_id=user_id, is_active=is_active), engine
    )


def vote_for(item_id: UUID4, user_id: UUID4, engine):
    return update_vote(item_id, user_id, engine)


def remove_vote_for(item_id: UUID4, user_id: UUID4, engine):
    return update_vote(item_id, user_id, engine, is_active=False)


def count_votes(item_id: UUID4, engine):
    with Session(engine) as session:
        rank = (
            func.rank()
            .over(order_by=Vote.create_ts.desc(), partition_by=Vote.user_id)
            .label("rnk")
        )
        inner = session.query(Vote, rank).where(Vote.item_id == item_id).subquery()
        outer = (
            select(inner.c.user_id)
            .where(and_(inner.c.rnk == 1, inner.c.is_active))
            .distinct()
            .subquery()
        )
        return session.query(outer).count()
