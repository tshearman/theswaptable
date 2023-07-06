from uuid import uuid4

from sqlmodel import Session
from backend.model import *
from backend.db.utils import truncate

user_ids = {
    "Richard Feynman": uuid4(),
    "Gary Gygax": uuid4(),
    "Mark Twain": uuid4(),
    "Bertrand Russell": uuid4(),
}


item_ids = {
    "Lectures in Physics": uuid4(),
    "Advanced Dungeons and Dragons": uuid4(),
    "Introduction to Gamma Convergence": uuid4(),
    "Connecticut Yankee": uuid4(),
}

item_types = [
    ItemType(id=ItemTypeId.GENERIC),
    ItemType(id=ItemTypeId.BOOK),
    ItemType(id=ItemTypeId.MODEL),
]

users = [
    User(
        id=user_ids["Richard Feynman"],
        name="Richard Feynman",
        email="feynman@lanl.gov",
    ),
    User(
        id=user_ids["Gary Gygax"],
        name="Gary Gygax",
        email="gygax@tsr.com",
    ),
    User(
        id=user_ids["Mark Twain"],
        name="Mark Twain",
        email="twain@steam.com",
    ),
    User(
        id=user_ids["Bertrand Russell"],
        name="Bertrand Russell",
        email="russell@trin.cam.ac.uk",
    ),
]

items = [
    Item(
        id=item_ids["Lectures in Physics"],
        type_id=ItemTypeId.BOOK,
        owner_id=user_ids["Richard Feynman"],
        title="Lectures in Physics",
    ),
    Item(
        id=item_ids["Advanced Dungeons and Dragons"],
        type_id=ItemTypeId.BOOK,
        owner_id=user_ids["Gary Gygax"],
        title="Advanced Dungeons and Dragons",
    ),
    Item(
        id=item_ids["Introduction to Gamma Convergence"],
        type_id=ItemTypeId.BOOK,
        owner_id=user_ids["Richard Feynman"],
        title="Introduction to Gamma Convergence",
    ),
    Item(
        id=item_ids["Connecticut Yankee"],
        type_id=ItemTypeId.BOOK,
        owner_id=user_ids["Mark Twain"],
        title="Connecticut Yankee",
        is_available=False,
    ),
]

votes = [
    Vote(
        item_id=item_ids["Lectures in Physics"],
        user_id=user_ids["Richard Feynman"],
    ),
    Vote(
        item_id=item_ids["Lectures in Physics"],
        user_id=user_ids["Gary Gygax"],
    ),
    Vote(
        item_id=item_ids["Advanced Dungeons and Dragons"],
        user_id=user_ids["Richard Feynman"],
    ),
    Vote(
        item_id=item_ids["Introduction to Gamma Convergence"],
        user_id=user_ids["Richard Feynman"],
    ),
    Vote(
        item_id=item_ids["Introduction to Gamma Convergence"],
        user_id=user_ids["Mark Twain"],
    ),
]


def setup(engine):
    def add_many(vs, session: Session):
        session.add_all(vs)
        return vs

    initialize_tables(engine)

    with Session(engine) as session:
        teardown(session)
        for values in [item_types, users, items, votes]:
            add_many(values, session)
            session.commit()


def teardown(session: Session):
    truncate(Vote, session, cascade=True)
    truncate(Item, session, cascade=True)
    truncate(User, session, cascade=True)
    truncate(ItemType, session, cascade=True)
    session.commit()
