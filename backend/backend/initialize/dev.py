from queries import generate_connection
from initialize.prod import initialize_tables
from model import ItemType, User, Item, Vote
from sqlalchemy.orm import Session


seed_item_types = [
    ItemType(0, "generic", "items"),
    ItemType(1, "book", "books"),
    ItemType(2, "model", "models"),
]

seed_users = [
    User("Richard Feynman", "feynman@lanl.gov", "abc123", id=1),
    User("Gary Gygax", "gygax@tsr.com", "def456", id=2),
]

seed_items = [
    Item(1, 1, "Lectures in Physics", id=101),
    Item(1, 2, "Advanced Dungeons and Dragons", id=102),
]

seed_votes = [Vote(101, 2), Vote(102, 1)]


def initialize():
    eng = generate_connection()
    initialize_tables(eng)
    for items in [seed_item_types, seed_users, seed_items, seed_votes]:
        with Session(eng) as session:
            session.add_all(items)
            session.commit()


if __name__ == "__main__":
    initialize()
