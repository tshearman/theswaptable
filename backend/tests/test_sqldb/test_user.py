from uuid import uuid4

from backend.sqldb import user
from tests.utils import DbTest


class TestDbUsers(DbTest):
    def test_read_all(self):
        users = user.read_all(self.session)
        assert len(users) == len(self.users)
        assert set([u.name for u in users]) == set(self.user_ids.keys())

    def test_count_all(self):
        assert user.count_all(self.session) == len(self.users)

    def test_read(self):
        for u in self.user_ids:
            assert user.read(self.session, id=self.user_ids[u]) is not None
        assert user.read(self.session, id=uuid4()) is None

    def test_read_by_email(self):
        for u in self.users:
            assert user.read_by_email(self.session, email=u.email) is not None
        assert user.read_by_email(self.session, email="villani@optimal.edu") is None
