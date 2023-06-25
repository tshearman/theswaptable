from backend.db.votes import post_vote, delete_vote
from backend.model import Vote
from sqlmodel import Session
from tests.utils import DbTest
from backend.db.mixed import count_votes


class TestDbMixed(DbTest):
    def test_count_votes(self):
        with Session(self.engine) as session:
            assert count_votes(self.item_ids["Lectures in Physics"], session) == 2
            assert (
                count_votes(self.item_ids["Advanced Dungeons and Dragons"], session)
                == 0
            )
            assert (
                count_votes(self.item_ids["Introduction to Gamma Convergence"], session)
                == 1
            )
            assert count_votes(self.item_ids["Connecticut Yankee"], session) == 0

    def test_vote_for(self):
        with Session(self.engine) as session:
            v = Vote(
                item_id=self.item_ids["Connecticut Yankee"],
                user_id=self.user_ids["Mark Twain"],
            )
            post_vote(v, session)
            assert count_votes(self.item_ids["Connecticut Yankee"], session) == 1

    def test_remove_vote_for(self):
        with Session(self.engine) as session:
            v = Vote(
                item_id=self.item_ids["Introduction to Gamma Convergence"],
                user_id=self.user_ids["Richard Feynman"],
            )
            delete_vote(v, session)
            assert (
                count_votes(self.item_ids["Introduction to Gamma Convergence"], session)
                == 0
            )
