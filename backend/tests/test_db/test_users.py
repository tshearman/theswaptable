from uuid import uuid4
from backend.db.users import count_users, lookup_user, lookup_user_by_email, add_user
from sqlmodel import Session
from tests.utils import DbTest


class TestDbUsers(DbTest):
    def test_add_user(self):
        with Session(self.engine) as session:
            num_users_start = count_users(session)
            add_user("Mary Oliver", "oliver@poets.com", "hij111213", session)
            num_users_after = count_users(session)
            assert (num_users_after - num_users_start) == 1

    def test_lookup_user_by_email(self):
        with Session(self.engine) as session:
            user = lookup_user_by_email("feynman@lanl.gov", session)
            assert user.name == "Richard Feynman"

    def test_lookup_user_exists(self):
        with Session(self.engine) as session:
            for user_id in self.user_ids:
                assert lookup_user(self.user_ids[user_id], session) is not None

    def test_lookup_user_nonexistent(self):
        with Session(self.engine) as session:
            assert lookup_user(uuid4(), session) is None
