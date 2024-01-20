from uuid import uuid4
from backend.sqldb import item
from tests.utils import DbTest
from backend.model import Item, ItemTypeId


class TestDbItem(DbTest):
    def test_read(self):
        for item_id in self.item_ids:
            out = item.read(self.session, id=self.item_ids[item_id])
            assert out is not None
            assert out.id == self.item_ids[item_id]
            assert out.title is not None
            assert not out.is_hidden
        assert item.read(self.session, id=uuid4()) is None

    def test_read_available(self):
        available_items = item.read_available(self.session)
        assert len(available_items) == len([i for i in self.items if i.is_available])

    def test_read_non_hidden(self):
        all_items = item.read_non_hidden(self.session)
        assert len(all_items) == len([i for i in self.items if not i.is_hidden])

    def test_read_all(self):
        all_items = item.read_all(self.session)
        assert len(all_items) == len(self.items)

    def test_read_user_library_by_user_id(self):
        max_library = -1
        for u in self.user_ids:
            library = item.read_user_library_by_user_id(
                self.session, user_id=self.user_ids[u]
            )
            assert len(library) >= 0
            max_library = max(max_library, len(library))
        assert max_library > 0

        assert (
            len(item.read_user_library_by_user_id(self.session, user_id=uuid4())) == 0
        )

    def test_read_all_paginated(self):
        first_items = item.read_all(self.session, offset=0, limit=2)
        second_items = item.read_all(self.session, offset=2, limit=2)
        first_ids = set([i.id for i in first_items])
        second_ids = set([i.id for i in second_items])

        assert len(first_items) <= 2
        assert len(second_items) <= 2
        assert first_ids.intersection(second_ids) == set()

    def test_create(self):
        id = uuid4()
        i = Item(
            id=id,
            owner_id=self.users[0].id,
            title="Waiting for Godot",
            author="Samuel Beckett",
            type_id=ItemTypeId.BOOK,
        )
        item.create(self.session, item=i)
        assert item.read(self.session, id=id) is not None

    def test_update(self):
        id = self.item_ids["Lectures in Physics"]
        i = item.update(self.session, id=id, author="Richard Feynman")
        assert item.read(self.session, id=id).author == "Richard Feynman"
        assert i.author == "Richard Feynman"

    def test_delete(self):
        id = self.item_ids["Lectures in Physics"]
        assert item.read(self.session, id=id) is not None
        item.delete(self.session, id=id)
        assert item.read(self.session, id=id) is None
