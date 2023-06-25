from backend.db.votes import (
    active_votes,
    users_votes,
)
from backend.model import Vote
from sqlmodel import Session
from tests.utils import DbTest


class TestDbVotes(DbTest):
    def test_active_votes(self):
        with Session(self.engine) as session:
            results = active_votes(session)
            assert len(results) == 3
            for result in results:
                assert type(result) == Vote

    def test_users_votes(self):
        with Session(self.engine) as session:
            user_votes_results = {
                user_id: users_votes(self.user_ids[user_id], session)
                for user_id in self.user_ids
            }
            assert len(user_votes_results) == len(self.user_ids)
            assert len(user_votes_results["Mark Twain"]) == 0
