import uuid
from backend.db.utils import add_many, count, truncate
from backend.utils import get_engine
from backend.db.voting import *
from backend.db.users import *
from backend.db.items import *
from backend.model import *
from abc import ABC


engine = get_engine()

user_ids = {
    "Richard Feynman": uuid.uuid4(),
    "Gary Gygax": uuid.uuid4(),
    "Mark Twain": uuid.uuid4(),
}

item_ids = {
    "Lectures in Physics": uuid.uuid4(),
    "Advanced Dungeons and Dragons": uuid.uuid4(),
    "Introduction to Gamma Convergence": uuid.uuid4(),
    "Connecticut Yankee": uuid.uuid4(),
}


def generate_item_types():
    return [
        ItemType(id=ItemTypeId.GENERIC, lookup_table="items"),
        ItemType(id=ItemTypeId.BOOK, lookup_table="books"),
        ItemType(id=ItemTypeId.MODEL, lookup_table="models"),
    ]


def generate_users():
    return [
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


def generate_items():
    return [
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


def generate_votes():
    return [
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


class DbTest(ABC):
    @classmethod
    def setup_class(cls):
        initialize_tables(engine)

    @classmethod
    def teardown_class(cls):
        drop_all_tables(engine)

    def setup_method(self, method):
        seed_item_types = generate_item_types()
        seed_users = generate_users()
        seed_items = generate_items()
        seed_votes = generate_votes()

        for items in [seed_item_types, seed_users, seed_items, seed_votes]:
            add_many(items, engine)

        assert count(ItemType, engine) == len(seed_item_types)
        assert count(User, engine) == len(seed_users)
        assert count(Item, engine) == len(seed_items)
        assert count(Vote, engine) == len(seed_votes)

    def teardown_method(self, method):
        truncate(Vote.__tablename__, engine, cascade=True)
        truncate(Item.__tablename__, engine, cascade=True)
        truncate(User.__tablename__, engine, cascade=True)
        truncate(ItemType.__tablename__, engine, cascade=True)

        assert count(Vote, engine) == 0
        assert count(Item, engine) == 0
        assert count(ItemType, engine) == 0
        assert count(User, engine) == 0


class TestDbVoting(DbTest):
    def test_count_votes(self):
        assert count_votes(item_ids["Lectures in Physics"], engine) == 2
        assert count_votes(item_ids["Advanced Dungeons and Dragons"], engine) == 0
        assert count_votes(item_ids["Introduction to Gamma Convergence"], engine) == 1
        assert count_votes(item_ids["Connecticut Yankee"], engine) == 0

    def test_vote_for(self):
        vote_for(
            item_ids["Connecticut Yankee"],
            user_ids["Mark Twain"],
            engine,
        )
        assert count_votes(item_ids["Connecticut Yankee"], engine) == 1

    def test_remove_vote_for(self):
        remove_vote_for(
            item_ids["Introduction to Gamma Convergence"],
            user_ids["Richard Feynman"],
            engine,
        )
        assert count_votes(item_ids["Introduction to Gamma Convergence"], engine) == 0


class TestDbUsers(DbTest):
    def test_add_user(self):
        num_users_start = count_users(engine)
        add_user("Mary Oliver", "oliver@poets.com", "hij111213", engine)
        num_users_after = count_users(engine)
        assert (num_users_after - num_users_start) == 1

    def test_lookup_user_by_email(self):
        user = lookup_user_by_email("feynman@lanl.gov", engine)
        assert user.name == "Richard Feynman"

    def test_lookup_user_exists(self):
        for user_id in user_ids:
            assert lookup_user(user_ids[user_id], engine) is not None
        assert lookup_user(uuid.uuid4(), engine) is None


class TestDbItems(DbTest):
    def test_lookup_item(self):
        for item_id in item_ids:
            assert lookup_item(item_ids[item_id], engine) is not None
        assert lookup_item(uuid.uuid4(), engine) is None
