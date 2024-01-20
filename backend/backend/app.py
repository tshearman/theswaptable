from fastapi import FastAPI
from sqlmodel import Session

from backend.devsetup import setup, teardown
from backend.external import goog
from backend.model import *
from backend.sqldb import user, item, vote
from backend.sqldb.utils import get_engine, get_google_search_app

app = FastAPI()
engine = get_engine()
google_app, google_token = get_google_search_app()


@app.on_event("startup")
def startup():
    setup(engine)


@app.on_event("shutdown")
def shutdown():
    with Session(engine) as session:
        teardown(session)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/")
async def read_users() -> list[User]:
    with Session(engine) as session:
        return user.read_all(session)


@app.get("/user/{id}")
async def read_user(id: UUID4) -> User:
    with Session(engine) as session:
        return user.read(session, id=id)


@app.get("/library/user/{id}")
async def read_user_library(id: UUID4) -> list[Item]:
    with Session(engine) as session:
        return item.read_user_library_by_user_id(session, user_id=id)


@app.delete("/user/{id}")
async def delete_user(id: UUID4) -> User:
    with Session(engine) as session:
        return user.delete(session, id=id)


@app.put("/users/")
async def create_user(u: User) -> User:
    with Session(engine) as session:
        return user.create(session, user=u)


@app.get("/items/")
async def read_items(
    available: bool | None = True, hidden: bool | None = False
) -> list[Item]:
    with Session(engine) as session:
        return item.read_conditional(session, available=available, hidden=hidden)


@app.get("/item/{id}")
async def read_item(id: UUID4) -> Item:
    with Session(engine) as session:
        return item.read(session, id=id)


@app.put("/item/")
async def create_item(i: Item) -> Item:
    with Session(engine, expire_on_commit=False) as session:
        return item.create(session, item=i)


@app.delete("/item/{id}")
async def delete_item(id: UUID4) -> Item:
    with Session(engine) as session:
        item.delete(session, id=id)


@app.put("/vote/")
async def create_vote(v: Vote) -> Vote:
    with Session(engine) as session:
        vote.create(session, vote=v)


@app.delete("/vote/{user_id}/{item_id}")
async def delete_vote(user_id: UUID4, item_id: UUID4) -> Vote:
    with Session(engine) as session:
        v = vote.read_by_user_and_item(session, user_id=user_id, item_id=item_id)
        return vote.delete(session, id=v.id)


@app.get("/item-votes/{id}")
async def count_item_votes(id: UUID4) -> int:
    with Session(engine) as session:
        return vote.count_votes_by_item_id(session, item_id=id)


@app.get("/items/voted-for-by/{id}")
async def read_user_votes(id: UUID4) -> list[Item]:
    with Session(engine) as session:
        vs: list[Vote] = vote.read_votes_by_user_id(session, user_id=id)
        return [item.read(session, id=v.item_id) for v in vs]


@app.get("/ext-images/")
async def get_image_recommendations(query: str, num: int = 5, page: int = 1):
    return goog.image_search(query, google_token, google_app, num=num, page=page)
