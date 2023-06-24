from backend.db.voting import (
    count_votes,
    vote,
    unvote,
    active_votes,
    users_votes,
)
from backend.db.items import user_voted_items
from backend.model import Vote, Item, User
from sqlmodel import Session
from tests.utils import DbTest


class TestDbVotes(DbTest):
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
            vote(
                self.item_ids["Connecticut Yankee"],
                self.user_ids["Mark Twain"],
                session,
            )
            assert count_votes(self.item_ids["Connecticut Yankee"], session) == 1

    def test_remove_vote_for(self):
        with Session(self.engine) as session:
            vote = Vote(
                item_id=self.item_ids["Introduction to Gamma Convergence"],
                user_id=self.user_ids["Richard Feynman"],
            )
            unvote(vote, session)
            assert (
                count_votes(self.item_ids["Introduction to Gamma Convergence"], session)
                == 0
            )

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

    def test_user_voted_items(self):
        with Session(self.engine) as session:
            results = user_voted_items(self.user_ids["Richard Feynman"], session)
            assert len(results) == 2
            for result in results:
                assert type(result[0]) == Item
                assert type(result[1]) == User
