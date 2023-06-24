from fastapi.testclient import TestClient
from backend.app import app
from uuid import uuid4
from backend.model import Vote
from tests.utils import DbTest


class TestApi(DbTest):
    def setup_method(self, _):
        super().setup_method(_)
        self.client = TestClient(app)

    def test_get_main(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_get_user(self):
        for user_id in self.user_ids:
            response = self.client.get(f"/user/{self.user_ids[user_id]}")
            assert response.status_code == 200
            assert response.json()["name"] == user_id

    def test_get_user_nonexisting(self):
        response = self.client.get(f"/user/{uuid4()}")
        assert response.status_code == 404

    def test_get_votes(self):
        for item_id in self.item_ids:
            response = self.client.get(f"/vote/{self.item_ids[item_id]}")
            assert response.status_code == 200
            assert response.json() >= 0

    def test_get_votes_nonexistent_item(self):
        response = self.client.get(f"/vote/{uuid4()}")
        assert response.status_code == 404

    def test_get_items(self):
        for item_id in self.item_ids:
            response = self.client.get(f"/item/{self.item_ids[item_id]}")
            assert response.status_code == 200

    def test_get_item_nonexistent(self):
        response = self.client.get(f"/item/{uuid4()}")
        assert response.status_code == 404

    def test_vote(self):
        for item in self.item_ids:
            for user in self.user_ids:
                item_id = self.item_ids[item]
                user_id = self.user_ids[user]
                num_votes_pre = self.client.get(f"/vote/{item_id}").json()
                response = self.client.post(f"/vote/{item_id}/{user_id}")
                assert response.status_code == 200
                num_votes_post = self.client.get(f"/vote/{item_id}").json()
                assert num_votes_post >= num_votes_pre

    def test_vote_valid(self):
        user_id = self.user_ids["Mark Twain"]
        item_id = self.item_ids["Connecticut Yankee"]
        assert self.client.get(f"/vote/{item_id}").json() == 0
        response = self.client.post(f"/vote/{item_id}/{user_id}")
        assert response.status_code == 200
        assert self.client.get(f"/vote/{item_id}").json() == 1

    def test_vote_invalid_item(self):
        user_id = self.user_ids["Mark Twain"]
        item_id = uuid4()
        response = self.client.post(f"/vote/{item_id}/{user_id}")
        assert response.status_code == 404
        assert "Item" in response.json()["detail"]

    def test_vote_invalid_user(self):
        user_id = uuid4()
        item_id = self.item_ids["Connecticut Yankee"]
        response = self.client.post(f"/vote/{item_id}/{user_id}")
        assert response.status_code == 404
        assert "User" in response.json()["detail"]
