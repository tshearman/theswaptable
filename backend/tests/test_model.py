from backend.model import Vote
from uuid import uuid4
from datetime import datetime


def test_voting_from_tuple():
    Vote.from_tuple((uuid4(), uuid4(), True, uuid4(), datetime.now()))
