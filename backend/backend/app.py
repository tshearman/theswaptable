from fastapi import FastAPI

from backend.external import goog
from backend.db.utils import get_engine, get_google_search_app


app = FastAPI()
engine = get_engine()
google_app, google_token = get_google_search_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.put("/item/")
# async def create_item(item: Item):
#     # Ensure that the associated user exists
#     await get_user(item.owner_id)

#     return with_session(engine, commit=True)(add_single)(item)


# @app.get("/item/{item_id}", response_model=Item)
# async def get_item(item_id: UUID4) -> Item | None:
#     return or404session(engine, "item")(items.get_item)(item_id)


# @app.post("/item/", response_model=Item)
# async def post_item(item: Item):
#     await get_user(item.owner_id)
#     return with_session(engine, commit=True, expire_on_commit=False)(add_single)(item)


# @app.delete("/item/", response_model=Item)
# async def delete_item(item: Item) -> Item:
#     return with_session(engine)(items.delete_item)(item)


# @app.get("/user/{user_id}", response_model=User | None)
# async def get_user(user_id: UUID4) -> User | None:
#     return or404session(engine, "user")(users.get_user)(user_id)


# @app.post("/user/")
# async def add_user(user: User):
#     return with_session(engine, commit=True)(add_single)(user)


# @app.get("/vote/{item_id}")
# async def get_item_vote_count(item_id: UUID4):
#     return or404session(engine, "item")(mixed.count_votes)(item_id)


# @app.get("/items/voted-by/{user_id}")
# async def get_user_votes(user_id: UUID4) -> list[Item]:
#     await get_user(user_id)
#     items = with_session(engine)(mixed.user_voted_items)(user_id)
#     return [item[0] for item in items]


# @app.post("/vote/{item_id}/{user_id}", response_model=Vote)
# async def post_vote(item_id: UUID4, user_id: UUID4):
#     vote = Vote(item_id=item_id, user_id=user_id)
#     await get_item(item_id)
#     await get_user(user_id)
#     return with_session(engine, commit=True, expire_on_commit=False)(votes.post_vote)(
#         vote
#     )


# @app.delete("/vote/{item_id}/{user_id}")
# async def delete_vote(item_id: UUID4, user_id: UUID4):
#     vote = Vote(item_id=item_id, user_id=user_id)
#     return with_session(engine, commit=True)(votes.delete_vote)(vote)


@app.get("/ext-images/")
async def get_image_recommendations(query, num=5, page=1):
    return goog.image_search(query, google_token, google_app, num=num, page=page)
