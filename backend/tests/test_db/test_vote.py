from tests.utils import DbTest
from backend.db import vote
from backend.model import Vote


class TestDbVotes(DbTest):
    def count_votes(self, title):
        return vote.count_votes_by_item_id(self.session, item_id=self.item_ids[title])

    def test_count(self):
        assert self.count_votes("Lectures in Physics") == 2
        assert self.count_votes("Advanced Dungeons and Dragons") == 1
        assert self.count_votes("Introduction to Gamma Convergence") == 2

    def test_create(self):
        user_id = self.user_ids["Bertrand Russell"]
        for item in self.item_ids:
            item_id = self.item_ids[item]
            num_votes = self.count_votes(item)
            vote.create(self.session, vote=Vote(item_id=item_id, user_id=user_id))
            assert self.count_votes(item) > num_votes

    def test_remove(self):
        for user in self.user_ids:
            votes = vote.read_votes_by_user_id(
                self.session, user_id=self.user_ids[user]
            )
            for v in votes:
                num_votes = vote.count_votes_by_item_id(self.session, item_id=v.item_id)
                vote.delete(self.session, id=v.id)
                num_votes_updated = vote.count_votes_by_item_id(
                    self.session, item_id=v.item_id
                )
                assert num_votes_updated < num_votes
