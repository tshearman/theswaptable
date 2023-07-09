from uuid import uuid4
from backend.db.utils import count, truncate
from backend.db.utils import get_engine
from backend.model import (
    ItemType,
    ItemTypeId,
    User,
    Vote,
    Item,
    drop_all_tables,
    initialize_tables,
)
from abc import ABC
from sqlmodel import Session, true


class DbTest(ABC):
    @staticmethod
    def generate_engine():
        return get_engine()

    def generate_user_ids(self):
        self.user_ids = {
            "Richard Feynman": uuid4(),
            "Gary Gygax": uuid4(),
            "Mark Twain": uuid4(),
            "Bertrand Russell": uuid4(),
        }

    def generate_item_ids(self):
        self.item_ids = {
            "Lectures in Physics": uuid4(),
            "Advanced Dungeons and Dragons": uuid4(),
            "Gamma Convergence for Beginners": uuid4(),
            "Connecticut Yankee": uuid4(),
        }

    def generate_vote_dicts(self, item_ids, user_ids):
        self.vote_dicts = [
            {
                "item_id": item_ids["Lectures in Physics"],
                "user_id": user_ids["Richard Feynman"],
            },
            {
                "item_id": item_ids["Lectures in Physics"],
                "user_id": user_ids["Gary Gygax"],
            },
            {
                "item_id": item_ids["Advanced Dungeons and Dragons"],
                "user_id": user_ids["Richard Feynman"],
            },
            {
                "item_id": item_ids["Gamma Convergence for Beginners"],
                "user_id": user_ids["Richard Feynman"],
            },
            {
                "item_id": item_ids["Gamma Convergence for Beginners"],
                "user_id": user_ids["Mark Twain"],
            },
        ]

    def generate_item_types(self):
        self.item_types = [
            ItemType(id=ItemTypeId.GENERIC),
            ItemType(id=ItemTypeId.BOOK),
            ItemType(id=ItemTypeId.MODEL),
        ]

    def generate_users(self, user_ids):
        self.users = [
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

    def generate_items(self, item_ids, user_ids):
        self.items = [
            Item(
                id=item_ids["Lectures in Physics"],
                type_id=ItemTypeId.BOOK,
                owner_id=user_ids["Richard Feynman"],
                title="Lectures in Physics",
                img_location="https://m.media-amazon.com/images/I/81m7QsFdp5L._AC_UF1000,1000_QL80_.jpg",
            ),
            Item(
                id=item_ids["Advanced Dungeons and Dragons"],
                type_id=ItemTypeId.BOOK,
                owner_id=user_ids["Gary Gygax"],
                title="Advanced Dungeons and Dragons",
                img_location="https://m.media-amazon.com/images/I/A1iyMzLoadL._AC_UF1000,1000_QL80_.jpg",
            ),
            Item(
                id=item_ids["Gamma Convergence for Beginners"],
                type_id=ItemTypeId.BOOK,
                owner_id=user_ids["Richard Feynman"],
                title="Gamma Convergence for Beginners",
                img_location="https://m.media-amazon.com/images/I/51fJxkKmlHL._AC_UF1000,1000_QL80_.jpg",
            ),
            Item(
                id=item_ids["Connecticut Yankee"],
                type_id=ItemTypeId.BOOK,
                owner_id=user_ids["Mark Twain"],
                title="Connecticut Yankee",
                is_available=False,
                img_location="https://m.media-amazon.com/images/I/51FfDxASpWL.jpg",
            ),
        ]

    def generate_votes(self):
        self.votes = list(map(lambda d: Vote(**d), self.vote_dicts))

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
        self.session = Session(self.engine)
        self.generate_item_ids()
        self.generate_user_ids()
        self.generate_item_types()
        self.generate_users(self.user_ids)
        self.generate_items(self.item_ids, self.user_ids)
        self.generate_vote_dicts(self.item_ids, self.user_ids)
        self.generate_votes()

        def add_many(vs, session: Session):
            session.add_all(vs)
            return vs

        # with Session(self.engine) as session:
        for items in [self.item_types, self.users, self.items, self.votes]:
            add_many(items, self.session)
            self.session.commit()

        # with Session(self.engine) as session:
        assert count(ItemType)(true)(self.session) == len(self.item_types)
        assert count(User)(true)(self.session) == len(self.users)
        assert count(Item)(true)(self.session) == len(self.items)
        assert count(Vote)(true)(self.session) == len(self.votes)

    def teardown_method(self, _):
        # with Session(self.engine) as session:
        truncate(Vote, self.session, cascade=True)
        truncate(Item, self.session, cascade=True)
        truncate(User, self.session, cascade=True)
        truncate(ItemType, self.session, cascade=True)
        self.session.commit()

        # with Session(self.engine) as session:
        assert count(Vote)(true)(self.session) == 0
        assert count(Item)(true)(self.session) == 0
        assert count(ItemType)(true)(self.session) == 0
        assert count(User)(true)(self.session) == 0
        self.session.close()
