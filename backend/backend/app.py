from fastapi import FastAPI
from sqlmodel import Session
from backend.utils import or404
from backend.db.users import lookup_user
from backend.model import Item, Vote, User
from backend.db.items import lookup_item, remove_item
from backend.db.voting import unvote
from backend.db.mixed import count_votes
from backend.db.utils import get_engine, add_single
from pydantic import UUID4

app = FastAPI()
engine = get_engine()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/item/{item_id}", response_model=Item)
async def read_item(item_id: UUID4) -> Item | None:
    with Session(engine) as session:
        return or404("item")(lookup_item)(item_id, session)


@app.post("/item/", response_model=Item)
async def add_item(item: Item):
    with Session(engine) as session:
        return add_single(item, session)


@app.delete("/item/", response_model=Item)
async def remove_item_(item: Item) -> Item:
    with Session(engine) as session:
        return remove_item(item, session)


@app.get("/user/{user_id}", response_model=User | None)
async def read_user(user_id: UUID4) -> User | None:
    with Session(engine) as session:
        return or404("user")(lookup_user)(user_id, session)


@app.post("/user/")
async def add_user(user: User):
    with Session(engine) as session:
        return add_single(user, session)


@app.get("/vote/{item_id}")
async def read_votes(item_id: UUID4):
    with Session(engine) as session:
        return or404("item")(count_votes)(item_id, session)


@app.post("/vote/")
async def cast_vote(vote: Vote):
    with Session(engine) as session:
        return add_single(vote, session)


@app.delete("/vote/")
async def remove_vote(vote: Vote):
    with Session(engine) as session:
        return unvote(vote, session)
