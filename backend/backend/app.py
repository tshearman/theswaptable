from fastapi import FastAPI
from backend.model import Item, Vote, User
from backend.db.items import lookup_item, remove_item
from backend.db.voting import count_votes
from backend.db.utils import get_engine, add_single
from pydantic import UUID4, EmailStr

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/add-item/")
async def add_item(item: Item):
    return add_single(item, get_engine())


@app.post("/add-vote/")
async def cast_vote(vote: Vote):
    return add_single(vote, get_engine())


@app.post("/add-user/")
async def add_user(user: User):
    return add_single(user, get_engine())


@app.post("/remove-vote/")
async def remove_vote(vote: Vote):
    vote.is_active = False
    return add_single(vote, get_engine())


@app.post("/remove-item/")
async def remove_item_(item: Item):
    return remove_item(item, get_engine())


@app.get("/items/{item_id}")
async def read_item(item_id: UUID4):
    return lookup_item(item_id, get_engine())


@app.get("/votes/{item_id}")
async def read_votes(item_id: UUID4):
    return count_votes(item_id, get_engine())
