from pydantic import UUID4
from sqlmodel import and_, not_, true, Session, false
from backend.model import Item
from backend.db import utils


@utils.all(Item)
def read_conditional(*, available: bool | None = True, hidden: bool | None = False):
    if available is None and hidden is None:
        return false
    if available is None and hidden:
        return Item.is_hidden
    if available is None and not hidden:
        return not_(Item.is_hidden)
    if available and hidden is None:
        return Item.is_available
    if available and hidden:
        return and_(Item.is_available, Item.is_hidden)
    if available and not hidden:
        return and_(Item.is_available, not_(Item.is_hidden))
    if not available and hidden is None:
        return not_(Item.is_available)
    if not available and hidden:
        return and_(not_(Item.is_available), Item.is_hidden)
    if not available and not hidden:
        return and_(not_(Item.is_available), not_(Item.is_hidden))


@utils.all(Item)
def read_all():
    return true


@utils.first(Item)
def read(*, id: UUID4):
    return Item.id == id


@utils.all(Item)
def read_available():
    return Item.is_available


@utils.all(Item)
def read_unavailable():
    return not_(Item.is_available)


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
