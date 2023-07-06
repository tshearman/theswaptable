from datetime import datetime
import uuid
from enum import Enum
from pydantic import UUID4, EmailStr, FileUrl, constr
from sqlmodel import Field, SQLModel, Relationship


class ItemTypeId(Enum):
    GENERIC = 0
    BOOK = 1
    MODEL = 2


class ItemType(SQLModel, table=True):
    __tablename__ = "dim_itemtypes"
    id: ItemTypeId = Field(default=ItemTypeId.GENERIC, primary_key=True)
    create_ts: datetime = Field(default_factory=datetime.now)


class User(SQLModel, table=True):
    __tablename__ = "users"
    name: str
    email: EmailStr = Field(unique=True)
    id: UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)
    is_hidden: bool = False
    create_ts: datetime = Field(default_factory=datetime.now)
    update_ts: datetime = Field(default_factory=datetime.now)


class UserAuth(SQLModel, table=True):
    __tablename__ = "user_auth"
    user_id: UUID4 = Field(foreign_key="users.id")
    id: UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)
    token: str | None = None


class Item(SQLModel, table=True):
    __tablename__ = "items"
    type_id: ItemTypeId = Field(foreign_key="dim_itemtypes.id")
    owner_id: UUID4 = Field(foreign_key="users.id")
    title: constr(min_length=1, max_length=248)
    is_available: bool = True
    is_hidden: bool = False
    author: str | None = None
    publisher: str | None = None
    isbn: str | None = None
    description: str | None = None
    img_location: FileUrl | None = None
    votes: list["Vote"] = Relationship(sa_relationship_kwargs={"cascade": "delete"})
    id: UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)
    create_ts: datetime = Field(default_factory=datetime.now)
    update_ts: datetime = Field(default_factory=datetime.now)


class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    item_id: UUID4 = Field(foreign_key="items.id")
    user_id: UUID4 = Field(foreign_key="users.id")
    id: UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)
    create_ts: datetime = Field(default_factory=datetime.now)
    update_ts: datetime = Field(default_factory=datetime.now)


class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    item_id: UUID4 = Field(foreign_key="items.id")
    user_id: UUID4 = Field(foreign_key="users.id")
    review: str
    id: UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)
    create_ts: datetime = Field(default_factory=datetime.now)
    update_ts: datetime = Field(default_factory=datetime.now)


class LendState(Enum):
    REQUESTED = 0
    ON_LOAN = 1
    RETURNED = 2


class Lend(SQLModel, table=True):
    __tablename__ = "lends"
    item_id: UUID4 = Field(foreign_key="items.id")
    borrower_id: UUID4 = Field(foreign_key="users.id")
    state: LendState
    id: UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)


def initialize_tables(engine):
    SQLModel.metadata.create_all(engine)


def drop_all_tables(engine):
    SQLModel.metadata.drop_all(engine)
