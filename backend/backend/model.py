import uuid
from datetime import datetime

from pydantic import BaseModel, validator, EmailStr, Field, UUID4


class User(BaseModel):
    name: str
    email: EmailStr
    id: UUID4 = Field(default_factory=uuid.uuid4)
    is_hidden: bool = False
    create_ts: datetime = Field(default_factory=datetime.now)
    update_ts: datetime = Field(default_factory=datetime.now)

    @validator("id")
    def validate_uuids(cls, value):
        return str(value)


class Item(BaseModel):
    title: str
    type_: str
    owner_id: UUID4
    id: UUID4 = Field(default_factory=uuid.uuid4)
    img_location: str | list[str] | None = None
    description: str | None = None
    is_hidden: bool = False
    is_available: bool = True
    create_ts: datetime = Field(default_factory=datetime.now)
    update_ts: datetime = Field(default_factory=datetime.now)

    @validator("id", "owner_id")
    def validate_uuids(cls, value):
        return str(value)


class Vote(BaseModel):
    item_id: UUID4
    user_id: UUID4


BOOK = "book"
MODEL = "model"
