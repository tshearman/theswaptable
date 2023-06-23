from fastapi import FastAPI
from sqlmodel import Session
from backend.model import Item, Vote, User
from backend.db.items import lookup_item, remove_item
from backend.db.voting import count_votes
from backend.db.utils import get_engine, add_single
from pydantic import UUID4

app = FastAPI()
engine = get_engine()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/add-item/")
async def add_item(item: Item):
    with Session(engine) as session:
        return add_single(item, session)


@app.post("/add-vote/")
async def cast_vote(vote: Vote):
    with Session(engine) as session:
        return add_single(vote, session)


@app.post("/add-user/")
async def add_user(user: User):
    with Session(engine) as session:
        return add_single(user, session)


@app.post("/remove-vote/")
async def remove_vote(vote: Vote):
    vote.is_active = False
    with Session(engine) as session:
        return add_single(vote, session)


@app.post("/remove-item/")
async def remove_item_(item: Item):
    with Session(engine) as session:
        return remove_item(item, session)


@app.get("/items/{item_id}")
async def read_item(item_id: UUID4):
    with Session(engine) as session:
        return lookup_item(item_id, session)


@app.get("/votes/{item_id}")
async def read_votes(item_id: UUID4):
    with Session(engine) as session:
        return count_votes(item_id, session)


@app.put("/update-token")
async def update_token(user: User):
    pass
