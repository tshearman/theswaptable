from fastapi import FastAPI
from backend.db.users import add_user
from backend.db.items import lookup_item
from backend.db.voting import remove_vote_for, vote_for, count_votes
from backend.utils import get_engine
from pydantic import UUID4, EmailStr

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: UUID4):
    return lookup_item(item_id, get_engine())


@app.get("/votes/{item_id}")
async def read_votes(item_id: UUID4):
    return count_votes(item_id, get_engine())


@app.put("/vote-for/{item_id}/{user_id}", response_model=bool)
async def cast_vote_for(item_id: UUID4, user_id: UUID4) -> bool:
    return vote_for(item_id, user_id, get_engine())


@app.put("/remove-vote-for/{item_id}/{user_id}", response_model=bool)
async def cast_vote_for(item_id: UUID4, user_id: UUID4) -> bool:
    return remove_vote_for(item_id, user_id, get_engine())


@app.put("/add-user/")
async def add_new_user(name: str, email: EmailStr, token: str) -> bool:
    return add_user(name, email, token, get_engine())
