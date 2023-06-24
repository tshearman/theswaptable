from uuid import uuid4
from backend.db.utils import add_many, count, truncate
from backend.db.utils import get_engine
from backend.db.voting import *
from backend.db.users import *
from backend.db.items import *
from backend.model import *
from abc import ABC
from sqlmodel import Session


class DbTest(ABC):
    @staticmethod
    def generate_engine():
        return get_engine()

    def generate_user_ids(self):
        self.user_ids = {
            "Richard Feynman": uuid4(),
            "Gary Gygax": uuid4(),
            "Mark Twain": uuid4(),
        }

    def generate_item_ids(self):
        self.item_ids = {
            "Lectures in Physics": uuid4(),
            "Advanced Dungeons and Dragons": uuid4(),
            "Introduction to Gamma Convergence": uuid4(),
            "Connecticut Yankee": uuid4(),
        }

    def generate_item_types(self):
        self.item_types = [
            ItemType(id=ItemTypeId.GENERIC, lookup_table="items"),
            ItemType(id=ItemTypeId.BOOK, lookup_table="books"),
            ItemType(id=ItemTypeId.MODEL, lookup_table="models"),
        ]

    def generate_users(self, user_ids):
        self.users = [
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

    def generate_items(self, item_ids, user_ids):
        self.items = [
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
            ),
        ]

    def generate_votes(self, item_ids, user_ids):
        self.votes = [
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
                create_ts=datetime(2023, 1, 1, 1, 0, 0, 0),
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
            Vote(
                item_id=item_ids["Introduction to Gamma Convergence"],
                user_id=user_ids["Mark Twain"],
                create_ts=datetime(2023, 1, 1, 2, 0, 0, 0),
                is_active=False,
            ),
        ]

    @classmethod
    def setup_class(cls):
        engine = cls.generate_engine()
        initialize_tables(engine)

    @classmethod
    def teardown_class(cls):
        engine = cls.generate_engine()
        drop_all_tables(engine)

    def setup_method(self, _):
        self.engine = DbTest.generate_engine()
        self.generate_item_ids()
        self.generate_user_ids()
        self.generate_item_types()
        self.generate_users(self.user_ids)
        self.generate_items(self.item_ids, self.user_ids)
        self.generate_votes(self.item_ids, self.user_ids)

        with Session(self.engine) as session:
            for items in [self.item_types, self.users, self.items, self.votes]:
                add_many(items, session)
                session.commit()

        with Session(self.engine) as session:
            assert count(ItemType, session) == len(self.item_types)
            assert count(User, session) == len(self.users)
            assert count(Item, session) == len(self.items)
            assert count(Vote, session) == len(self.votes)

    def teardown_method(self, _):
        with Session(self.engine) as session:
            truncate(Vote.__tablename__, session, cascade=True)
            truncate(Item.__tablename__, session, cascade=True)
            truncate(User.__tablename__, session, cascade=True)
            truncate(ItemType.__tablename__, session, cascade=True)
            session.commit()

        with Session(self.engine) as session:
            assert count(Vote, session) == 0
            assert count(Item, session) == 0
            assert count(ItemType, session) == 0
            assert count(User, session) == 0
