from fastapi.testclient import TestClient
from backend.app import app
from backend.model import Vote
from backend.db.utils import add_single
from backend.model import Item, ItemTypeId
from uuid import uuid4
from tests.utils import DbTest
from backend.utils import with_session
from backend.db.items import lookup_item
import json


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

    # def test_add_item(self):
    #     item_id = uuid4()
    #     assert with_session(self.engine)(lookup_item)(item_id) is None

    #     item = Item(
    #         type_id=ItemTypeId.BOOK,
    #         owner_id=self.user_ids["Richard Feynman"],
    #         title="Optimal Transport: Old and New",
    #         id=item_id
    #     )
    #     d = json.loads(item.json())

    #     response = self.client.post("/item/", json=d)
    #     assert response.status_code == 200

    # v = Vote()
    # def test_vote_post(self):
    #     self.client.post("/vote", )
