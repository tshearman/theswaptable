import uuid
from backend.db.utils import add_many, count, truncate
from backend.db.utils import get_engine
from backend.db.voting import *
from backend.db.users import *
from backend.db.items import *
from backend.model import *
from abc import ABC
from sqlmodel import Session


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


class DbTest(ABC):
    @classmethod
    def setup_class(cls):
        initialize_tables(engine)

    @classmethod
    def teardown_class(cls):
        drop_all_tables(engine)

    def setup_method(self, _):
        seed_item_types = generate_item_types()
        seed_users = generate_users()
        seed_items = generate_items()
        seed_votes = generate_votes()

        with Session(engine) as session:
            for items in [seed_item_types, seed_users, seed_items, seed_votes]:
                add_many(items, session)

            assert count(ItemType, session) == len(seed_item_types)
            assert count(User, session) == len(seed_users)
            assert count(Item, session) == len(seed_items)
            assert count(Vote, session) == len(seed_votes)

    def teardown_method(self, _):
        with Session(engine) as session:
            truncate(Vote.__tablename__, session, cascade=True)
            truncate(Item.__tablename__, session, cascade=True)
            truncate(User.__tablename__, session, cascade=True)
            truncate(ItemType.__tablename__, session, cascade=True)

            assert count(Vote, session) == 0
            assert count(Item, session) == 0
            assert count(ItemType, session) == 0
            assert count(User, session) == 0


class TestDbVotes(DbTest):
    def test_count_votes(self):
        with Session(engine) as session:
            assert count_votes(item_ids["Lectures in Physics"], session) == 2
            assert count_votes(item_ids["Advanced Dungeons and Dragons"], session) == 0
            assert (
                count_votes(item_ids["Introduction to Gamma Convergence"], session) == 1
            )
            assert count_votes(item_ids["Connecticut Yankee"], session) == 0

    def test_vote_for(self):
        with Session(engine) as session:
            vote_for(
                item_ids["Connecticut Yankee"],
                user_ids["Mark Twain"],
                session,
            )
            assert count_votes(item_ids["Connecticut Yankee"], session) == 1

    def test_remove_vote_for(self):
        with Session(engine) as session:
            remove_vote_for(
                item_ids["Introduction to Gamma Convergence"],
                user_ids["Richard Feynman"],
                session,
            )
            assert (
                count_votes(item_ids["Introduction to Gamma Convergence"], session) == 0
            )

    def test_active_votes(self):
        with Session(engine) as session:
            results = active_votes(session)
            assert len(results) == 3
            for result in results:
                assert type(result) == Vote

    def test_users_votes(self):
        with Session(engine) as session:
            user_votes_results = {
                user_id: users_votes(user_ids[user_id], session) for user_id in user_ids
            }
            assert len(user_votes_results) == len(user_ids)
            assert len(user_votes_results["Mark Twain"]) == 0

    def test_user_voted_items(self):
        with Session(engine) as session:
            results = user_voted_items(user_ids["Richard Feynman"], session)
            assert len(results) == 2
            for result in results:
                assert type(result[0]) == Item
                assert type(result[1]) == User


class TestDbUsers(DbTest):
    def test_add_user(self):
        with Session(engine) as session:
            num_users_start = count_users(session)
            add_user("Mary Oliver", "oliver@poets.com", "hij111213", session)
            num_users_after = count_users(session)
            assert (num_users_after - num_users_start) == 1

    def test_lookup_user_by_email(self):
        with Session(engine) as session:
            user = lookup_user_by_email("feynman@lanl.gov", session)
            assert user.name == "Richard Feynman"

    def test_lookup_user_exists(self):
        with Session(engine) as session:
            for user_id in user_ids:
                assert lookup_user(user_ids[user_id], session) is not None
            assert lookup_user(uuid.uuid4(), session) is None


class TestDbItems(DbTest):
    def test_lookup_item(self):
        with Session(engine) as session:
            for item_id in item_ids:
                assert lookup_item(item_ids[item_id], session) is not None
            assert lookup_item(uuid.uuid4(), session) is None

    def test_lookup_user_library(self):
        with Session(engine) as session:
            for user_id in user_ids:
                assert len(lookup_user_library(user_ids[user_id], session)) >= 1
            assert len(lookup_user_library(uuid.uuid4(), session)) == 0

    def test_items(self):
        with Session(engine) as session:
            results = items(session)
            assert len(set(item_ids.values())) == 4
            assert len(results) == 4
            assert len(set([item.id for (item, _) in results])) == len(item_ids)

    def test_items_paginated(self):
        with Session(engine) as session:
            results_one = items_paginated(2, 0, session)
            results_two = items_paginated(2, 2, session)
            assert len(results_one) == 2
            assert len(results_two) == 2
            assert set([r[0].id for r in results_one]).isdisjoint(
                set([r[0].id for r in results_two])
            )

    def test_remove_item(self):
        with Session(engine) as session:
            for item_id in item_ids:
                assert lookup_item(item_ids[item_id], session) is not None

            for item_id in item_ids:
                item = lookup_item(item_ids[item_id], session)
                remove_item(item, session)

            for item_id in item_ids:
                assert lookup_item(item_ids[item_id], session) is None
