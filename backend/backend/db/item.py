from pydantic import UUID4
from sqlmodel import and_, not_, true, Session
from backend.model import Item
from backend.db import utils


@utils.all(Item)
def read_all():
    return true()


@utils.first(Item)
def read(*, id: UUID4):
    return Item.id == id


@utils.all(Item)
def read_available():
    return Item.is_available


@utils.all(Item)
def read_non_hidden():
    return not_(Item.is_hidden)


@utils.all(Item)
def read_available_non_hidden():
    return and_(Item.is_available, not_(Item.is_hidden))


@utils.all(Item)
def read_user_library_by_user_id(*, user_id: UUID4):
    return and_(Item.owner_id == user_id)


def create(session: Session, *, item: Item) -> Item:
    return utils.create(Item)(session, item)


def update(session: Session, *, id: UUID4, **kwargs) -> Item:
    return utils.update(Item, read)(session, id=id, **kwargs)


def delete(session: Session, *, id: UUID4) -> Item:
    return utils.delete(Item, read)(session, id=id)


def toggle_availability(session: Session, *, item: Item) -> Item:
    return update(session, id=item.id, is_available=not item.is_available)


def is_unavailable(session: Session, *, item: Item) -> Item:
    return update(session, id=item.id, is_available=False)


def is_available(session: Session, *, item: Item) -> Item:
    return update(session, id=item.id, is_available=True)
