from pydantic import UUID4
from sqlmodel import select, Session
from backend.model import Item


def lookup_item(item_id: UUID4, engine) -> Item | None:
    with Session(engine) as session:
        return session.execute(select(Item).where(Item.id == item_id)).first()
