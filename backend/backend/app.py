from fastapi import FastAPI
from db.users import add_user
from db.voting import remove_vote_for, vote_for, count_votes
from initialize.prod import get_engine

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return {"item_id": item_id}


@app.get("/votes/{item_id}")
async def read_votes(item_id: str):
    return count_votes(item_id, get_engine())


@app.put("/vote-for/{item_id}/{user_id}")
async def cast_vote_for(item_id: str, user_id: str) -> bool:
    return vote_for(item_id, user_id, get_engine())


@app.put("/unvote-for/{item_id}/{user_id}")
async def cast_vote_for(item_id: str, user_id: str) -> bool:
    return remove_vote_for(item_id, user_id, get_engine())


@app.put("/new-user/")
async def add_new_user(name: str, email: str, token: str) -> bool:
    return add_user(name, email, token, get_engine())
