from db.utils import add_many
from db.voting import remove_vote_for, vote_for, count_votes
from initialize.prod import initialize_tables, get_engine
from model import ItemType, User, Item, Vote
from model import ItemTypeId
from datetime import datetime
import uuid


seed_item_types = [
    ItemType(id=ItemTypeId.GENERIC, lookup_table="items"),
    ItemType(id=ItemTypeId.BOOK, lookup_table="books"),
    ItemType(id=ItemTypeId.MODEL, lookup_table="models"),
]

user_ids = {
    "Richard Feynman": uuid.uuid4(),
    "Gary Gygax": uuid.uuid4(),
    "Mark Twain": uuid.uuid4(),
}
seed_users = [
    User(
        id=user_ids["Richard Feynman"],
        name="Richard Feynman",
        email="feynman@lanl.gov",
        token="abc123",
    ),
    User(
        id=user_ids["Gary Gygax"],
        name="Gary Gygax",
        email="gygax@tsr.com",
        token="def456",
    ),
    User(
        id=user_ids["Mark Twain"],
        name="Mark Twain",
        email="twain@steam.com",
        token="fgh789",
    ),
]

item_ids = {
    "Lectures in Physics": uuid.uuid4(),
    "Advanced Dungeons and Dragons": uuid.uuid4(),
    "Introduction to Gamma Convergence": uuid.uuid4(),
    "Connecticut Yankee in King Arthur's Court": uuid.uuid4(),
}
seed_items = [
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
        id=item_ids["Connecticut Yankee in King Arthur's Court"],
        type_id=ItemTypeId.BOOK,
        owner_id=user_ids["Mark Twain"],
        title="Connecticut Yankee in King Arthur's Court",
    ),
]

seed_votes = [
    Vote(
        item_id=item_ids["Lectures in Physics"],
        user_id=user_ids["Richard Feynman"],
        create_ts=datetime(2023, 1, 1, 2, 30, 0, 0),
    ),
    Vote(
        item_id=item_ids["Lectures in Physics"],
        user_id=user_ids["Gary Gygax"],
        create_ts=datetime(2023, 1, 1, 1, 30, 0, 0),
    ),
    Vote(
        item_id=item_ids["Lectures in Physics"],
        user_id=user_ids["Gary Gygax"],
        create_ts=datetime(2023, 1, 1, 1, 0, 0, 0),
    ),
    Vote(
        item_id=item_ids["Advanced Dungeons and Dragons"],
        user_id=user_ids["Richard Feynman"],
        create_ts=datetime(2023, 1, 1, 2, 30, 0, 0),
        is_active=False,
    ),
    Vote(
        item_id=item_ids["Advanced Dungeons and Dragons"],
        user_id=user_ids["Richard Feynman"],
        create_ts=datetime(2023, 1, 1, 2, 0, 0, 0),
    ),
    Vote(
        item_id=item_ids["Introduction to Gamma Convergence"],
        user_id=user_ids["Richard Feynman"],
        create_ts=datetime(2023, 1, 1, 2, 0, 0, 0),
    ),
    Vote(
        item_id=item_ids["Introduction to Gamma Convergence"],
        user_id=user_ids["Richard Feynman"],
        create_ts=datetime(2023, 1, 1, 2, 0, 0, 0),
    ),
]


def init():
    engine = get_engine()
    initialize_tables(engine)
    for items in [seed_item_types, seed_users, seed_items, seed_votes]:
        add_many(items, engine)


if __name__ == "__main__":
    init()
    e = get_engine()
    assert count_votes(item_ids["Lectures in Physics"], e) == 2
    assert count_votes(item_ids["Advanced Dungeons and Dragons"], e) == 0
    assert count_votes(item_ids["Introduction to Gamma Convergence"], e) == 1
    assert count_votes(item_ids["Connecticut Yankee in King Arthur's Court"], e) == 0

    vote_for(
        item_ids["Connecticut Yankee in King Arthur's Court"], user_ids["Mark Twain"], e
    )
    assert count_votes(item_ids["Connecticut Yankee in King Arthur's Court"], e) == 1

    remove_vote_for(
        item_ids["Connecticut Yankee in King Arthur's Court"], user_ids["Mark Twain"], e
    )
    assert count_votes(item_ids["Connecticut Yankee in King Arthur's Court"], e) == 0
