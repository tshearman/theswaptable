from tests.utils import DbTest
from backend.sqldb import shared


class TestDbMixed(DbTest):
    def test_read_user_votes(self):
        for u in self.users:
            assert len(shared.read_user_votes(self.session, user=u)) >= 0


#     @pytest.mark.skip
#     def test_count_votes(self):
#         with Session(self.engine) as session:
#             assert count_votes(self.item_ids["Lectures in Physics"], session) == 2
#             assert (
#                 count_votes(self.item_ids["Advanced Dungeons and Dragons"], session)
#                 == 0
#             )
#             assert (
#                 count_votes(self.item_ids["Introduction to Gamma Convergence"], session)
#                 == 1
#             )
#             assert count_votes(self.item_ids["Connecticut Yankee"], session) == 0


#     @pytest.mark.skip
#     def test_vote_for(self):
#         with Session(self.engine) as session:
#             v = Vote(
#                 item_id=self.item_ids["Connecticut Yankee"],
#                 user_id=self.user_ids["Mark Twain"],
#             )
#             post_vote(v, session)
#             assert count_votes(self.item_ids["Connecticut Yankee"], session) == 1


#     @pytest.mark.skip
#     def test_remove_vote_for(self):
#         with Session(self.engine) as session:
#             v = Vote(
#                 item_id=self.item_ids["Introduction to Gamma Convergence"],
#                 user_id=self.user_ids["Richard Feynman"],
#             )
#             delete_vote(v, session)
#             assert (
#                 count_votes(self.item_ids["Introduction to Gamma Convergence"], session)
#                 == 0
#             )


#     @pytest.mark.skip
#     def test_user_voted_items(self):
#         with Session(self.engine) as session:
#             results = user_voted_items(self.user_ids["Richard Feynman"], session)
#             assert len(results) == 2
#             for result in results:
#                 assert type(result[0]) == Item
#                 assert type(result[1]) == User
