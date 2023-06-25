from fastapi import FastAPI
from sqlmodel import Session
from backend.utils import or404
from backend.db import users, items, mixed, votes
from backend.model import Item, Vote, User
from backend.db.utils import get_engine, add_single
from pydantic import UUID4

app = FastAPI()
engine = get_engine()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/item/{item_id}", response_model=Item)
async def get_item(item_id: UUID4) -> Item | None:
    with Session(engine) as session:
        return or404("item")(items.get_item)(item_id, session)


@app.post("/item/", response_model=Item)
async def add_item(item: Item):
    with Session(engine) as session:
        return add_single(item, session)


@app.delete("/item/", response_model=Item)
async def delete_item(item: Item) -> Item:
    with Session(engine) as session:
        return items.delete_item(item, session)


@app.get("/user/{user_id}", response_model=User | None)
async def get_user(user_id: UUID4) -> User | None:
    with Session(engine) as session:
        return or404("user")(users.get_user)(user_id, session)


@app.post("/user/")
async def add_user(user: User):
    with Session(engine) as session:
        return add_single(user, session)


@app.get("/vote/{item_id}")
async def get_item_vote_count(item_id: UUID4):
    with Session(engine) as session:
        return or404("item")(mixed.count_votes)(item_id, session)


@app.post("/vote/{item_id}/{user_id}", response_model=Vote)
async def post_vote(item_id: UUID4, user_id: UUID4):
    await get_item(item_id)
    await get_user(user_id)
    with Session(engine, expire_on_commit=False) as session:
        v = Vote(item_id=item_id, user_id=user_id)
        response = votes.post_vote(v, session)
        session.commit()
        return response


@app.delete("/vote/")
async def delete_vote(v: Vote):
    with Session(engine) as session:
        return votes.delete_vote(v, session)
