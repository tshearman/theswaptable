from fastapi.testclient import TestClient
from backend.app import app


class TestApi:
    def setup_method(self, _):
        # super().setup_method(_)
        self.client = TestClient(app)

    def test_get_main(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    # @pytest.mark.skip
    # def test_get_user(self):
    #     for user_id in self.user_ids:
    #         response = self.client.get(f"/user/{self.user_ids[user_id]}")
    #         assert response.status_code == 200
    #         assert response.json()["name"] == user_id

    # @pytest.mark.skip
    # def test_get_user_nonexisting(self):
    #     response = self.client.get(f"/user/{uuid4()}")
    #     assert response.status_code == 404

    # @pytest.mark.skip
    # def test_get_votes(self):
    #     for item_id in self.item_ids:
    #         response = self.client.get(f"/vote/{self.item_ids[item_id]}")
    #         assert response.status_code == 200
    #         assert response.json() >= 0

    # @pytest.mark.skip
    # def test_get_votes_nonexistent_item(self):
    #     response = self.client.get(f"/vote/{uuid4()}")
    #     assert response.status_code == 404

    # @pytest.mark.skip
    # def test_get_items(self):
    #     for item_id in self.item_ids:
    #         response = self.client.get(f"/item/{self.item_ids[item_id]}")
    #         assert response.status_code == 200

    # @pytest.mark.skip
    # def test_get_item_nonexistent(self):
    #     response = self.client.get(f"/item/{uuid4()}")
    #     assert response.status_code == 404

    # @pytest.mark.skip
    # def test_post_vote(self):
    #     for item in self.item_ids:
    #         for user in self.user_ids:
    #             item_id = self.item_ids[item]
    #             user_id = self.user_ids[user]
    #             num_votes_pre = self.client.get(f"/vote/{item_id}").json()
    #             response = self.client.post(f"/vote/{item_id}/{user_id}")
    #             assert response.status_code == 200
    #             num_votes_post = self.client.get(f"/vote/{item_id}").json()
    #             assert num_votes_post >= num_votes_pre

    # @pytest.mark.skip
    # def test_post_vote_valid(self):
    #     user_id = self.user_ids["Mark Twain"]
    #     item_id = self.item_ids["Connecticut Yankee"]
    #     assert self.client.get(f"/vote/{item_id}").json() == 0
    #     response = self.client.post(f"/vote/{item_id}/{user_id}")
    #     assert response.status_code == 200
    #     assert self.client.get(f"/vote/{item_id}").json() == 1

    # @pytest.mark.skip
    # def test_post_vote_invalid_item(self):
    #     user_id = self.user_ids["Mark Twain"]
    #     item_id = uuid4()
    #     response = self.client.post(f"/vote/{item_id}/{user_id}")
    #     assert response.status_code == 404
    #     assert "Item" in response.json()["detail"]

    # @pytest.mark.skip
    # def test_post_vote_invalid_user(self):
    #     user_id = uuid4()
    #     item_id = self.item_ids["Connecticut Yankee"]
    #     response = self.client.post(f"/vote/{item_id}/{user_id}")
    #     assert response.status_code == 404
    #     assert "User" in response.json()["detail"]

    # @pytest.mark.skip
    # def test_post_user(self):
    #     user = User(
    #         name="Robert Matthew Van Winkle",
    #         email="vanillaice@gmail.com",
    #         auth_token="ice-ice-baby",
    #     )
    #     post_response = self.client.post("/user", content=user.json())
    #     assert post_response.status_code == 200
    #     get_response = self.client.get(f"/user/{user.id}")
    #     assert get_response.status_code == 200

    # @pytest.mark.skip
    # def test_post_user_exists(self):
    #     for user in self.users:
    #         response = self.client.post("/user", content=user.json())
    #         assert response.status_code != 200

    # @pytest.mark.skip
    # def test_delete_vote_valid(self):
    #     item_id = self.item_ids["Lectures in Physics"]
    #     user_id = self.user_ids["Richard Feynman"]
    #     vote_count = self.client.get(f"/vote/{item_id}").json()
    #     self.client.delete(f"/vote/{item_id}/{user_id}")
    #     updated_vote_count = self.client.get(f"/vote/{item_id}").json()
    #     assert updated_vote_count < vote_count

    # @pytest.mark.skip
    # def test_delete_vote_all(self):
    #     for vote in self.vote_dicts:
    #         self.client.delete(f"/vote/{vote['item_id']}/{vote['user_id']}")

    #     for item in self.item_ids:
    #         assert self.client.get(f"/vote/{self.item_ids[item]}").json() == 0

    # @pytest.mark.skip
    # def test_get_items_user_voted_for_valid(self):
    #     user_id = self.user_ids["Richard Feynman"]
    #     response = self.client.get(f"/items/voted-by/{user_id}")
    #     assert len(response.json()) == 2

    # @pytest.mark.skip
    # def test_get_items_user_voted_for_all(self):
    #     for user in self.user_ids:
    #         user_id = self.user_ids[user]
    #         response = self.client.get(f"/items/voted-by/{user_id}")
    #         assert response.status_code == 200

    # @pytest.mark.skip
    # def test_get_items_user_voted_for_invalid_user(self):
    #     user_id = uuid4()
    #     response = self.client.get(f"/items/voted-by/{user_id}")
    #     assert response.status_code == 404

    # @pytest.mark.skip
    # def test_post_item(self):
    #     owner_id = self.user_ids["Richard Feynman"]
    #     item_id = uuid4()
    #     item = Item(
    #         type_id=ItemTypeId.GENERIC, owner_id=owner_id, title="Mork Borg", id=item_id
    #     )
    #     post_response = self.client.post("/item", content=item.json())
    #     assert post_response.status_code == 200
    #     get_response = self.client.get(f"/item/{item_id}")
    #     assert get_response.status_code == 200

    # @pytest.mark.skip
    # @pytest.mark.external
    # def test_get_google_images(self):
    #     response = self.client.get("/ext-images/", params={"query": "Morg Borg"})
    #     assert response.status_code == 200
