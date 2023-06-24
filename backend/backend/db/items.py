from pydantic import UUID4, constr, FileUrl
from sqlmodel import select, func, and_
from backend.db.utils import add_single
from backend.model import Item, User, ItemTypeId


def add_item(
    session,
    type_id: ItemTypeId,
    owner_id: UUID4,
    title: constr(min_length=1, max_length=248),
    description: str | None = None,
    img_location: FileUrl | None = None,
):
    item = Item(
        type_id=type_id,
        owner_id=owner_id,
        title=title,
        description=description,
        img_location=img_location,
    )
    add_single(item, session)


def remove_item(item: Item, session):
    the_item = session.exec(select(Item).where(Item.id == item.id)).one()
    the_item.is_active = False
    session.add(the_item)
    session.commit()


def lookup_item(item_id: UUID4, session) -> Item | None:
    inner = active_items_query(session)
    result = session.exec(
        select(*Item.from_query(inner)).where(inner.c.id == item_id)
    ).first()
    if result:
        return Item.from_tuple(result)
    return None


def all_items_query(session):
    inner = active_items_query(session)
    return select(*Item.from_query(inner), User).join(
        User, onclause=inner.c.owner_id == User.id
    )


def _parse_item_from_item_user_result(result):
    return (Item.from_tuple(result[:8]), result[8])


def _parse_items_results_(results) -> list[(Item, User)]:
    return list(map(_parse_item_from_item_user_result, results))


def items(session):
    results = session.exec(all_items_query(session)).all()
    return _parse_items_results_(results)


def items_paginated(limit: int, offset: int, session) -> list[(Item, User)]:
    results = session.exec(all_items_query(session).offset(offset).limit(limit)).all()
    return _parse_items_results_(results)


def lookup_user_library(user_id: UUID4, session) -> list[Item]:
    return session.exec(select(Item).where(Item.owner_id == user_id)).all()


def active_items_query(session):
    rank = (
        func.rank()
        .over(
            order_by=[Item.create_ts.desc(), func.random()],
            partition_by=[Item.id],
        )
        .label("rnk")
    )
    inner = session.query(Item, rank).subquery()
    return (
        select(*Item.from_query(inner))
        .join(User, onclause=inner.c.owner_id == User.id)
        .where(and_(inner.c.rnk == 1, inner.c.is_active))
        .subquery()
    )
