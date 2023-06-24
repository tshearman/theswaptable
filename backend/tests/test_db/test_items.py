import uuid
from backend.db.items import (
    items,
    lookup_item,
    lookup_user_library,
    items_paginated,
    remove_item,
)
from sqlmodel import Session
from tests.utils import DbTest


class TestDbItems(DbTest):
    def test_lookup_item(self):
        with Session(self.engine) as session:
            for item_id in self.item_ids:
                assert lookup_item(self.item_ids[item_id], session) is not None
            assert lookup_item(uuid.uuid4(), session) is None

    def test_lookup_user_library(self):
        with Session(self.engine) as session:
            for user_id in self.user_ids:
                assert len(lookup_user_library(self.user_ids[user_id], session)) >= 1
            assert len(lookup_user_library(uuid.uuid4(), session)) == 0

    def test_items(self):
        with Session(self.engine) as session:
            results = items(session)
            assert len(set(self.item_ids.values())) == 4
            assert len(results) == 4
            assert len(set([item.id for (item, _) in results])) == len(self.item_ids)

    def test_items_paginated(self):
        with Session(self.engine) as session:
            results_one = items_paginated(2, 0, session)
            results_two = items_paginated(2, 2, session)
            assert len(results_one) == 2
            assert len(results_two) == 2
            assert set([r[0].id for r in results_one]).isdisjoint(
                set([r[0].id for r in results_two])
            )

    def test_remove_item(self):
        with Session(self.engine) as session:
            for item_id in self.item_ids:
                assert lookup_item(self.item_ids[item_id], session) is not None

            for item_id in self.item_ids:
                item = lookup_item(self.item_ids[item_id], session)
                remove_item(item, session)

            for item_id in self.item_ids:
                assert lookup_item(self.item_ids[item_id], session) is None
