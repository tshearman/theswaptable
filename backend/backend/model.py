from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field, UUID4


class User(BaseModel):
    name: str
    email: EmailStr
    id: UUID4 = Field(default_factory=uuid4)
    is_hidden: bool = False
    create_ts: datetime = Field(default_factory=datetime.now)
    update_ts: datetime = Field(default_factory=datetime.now)


class Item(BaseModel):
    title: str
    type_: str
    owner_id: UUID4
    id: UUID4 = Field(default_factory=uuid4)
    img_location: str | list[str] | None = None
    description: str | None = None
    is_hidden: bool = False
    is_available: bool = True
    create_ts: datetime = Field(default_factory=datetime.now)
    update_ts: datetime = Field(default_factory=datetime.now)


class Vote(BaseModel):
    item_id: UUID4
    user_id: UUID4


BOOK = "book"
MODEL = "model"
