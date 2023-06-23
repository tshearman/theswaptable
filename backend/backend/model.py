from datetime import datetime
import uuid
from enum import Enum
from pydantic import UUID4, EmailStr, FileUrl, constr
from sqlmodel import Field, SQLModel


class ItemTypeId(Enum):
    GENERIC = 0
    BOOK = 1
    MODEL = 2


class ItemType(SQLModel, table=True):
    __tablename__ = "dim_itemtypes"
    lookup_table: str
    id: ItemTypeId = Field(default=ItemTypeId.GENERIC, primary_key=True)
    create_ts: datetime = Field(default_factory=datetime.now)


class User(SQLModel, table=True):
    __tablename__ = "users"
    name: str
    email: EmailStr = Field(unique=True)
    token: str
    id: UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)
    create_ts: datetime = Field(default_factory=datetime.now)


class Item(SQLModel, table=True):
    __tablename__ = "items"
    type_id: ItemTypeId = Field(foreign_key="dim_itemtypes.id")
    owner_id: UUID4 = Field(foreign_key="users.id")
    title: constr(min_length=1, max_length=248)
    description: str | None = None
    img_location: FileUrl | None = None
    is_active: bool = True
    id: UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)
    create_ts: datetime = Field(default_factory=datetime.now)


class BookDetails(SQLModel, table=True):
    __tablename__ = "books"
    author: str | None = None
    publisher: str | None = None
    isbn: str | None = None
    id: UUID4 = Field(foreign_key="items.id", primary_key=True)
    create_ts: datetime = Field(default_factory=datetime.now)


class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    item_id: UUID4 = Field(foreign_key="items.id")
    user_id: UUID4 = Field(foreign_key="users.id")
    is_active: bool = True
    id: UUID4 = Field(primary_key=True, default_factory=uuid.uuid4)
    create_ts: datetime = Field(default_factory=datetime.now)


def initialize_tables(engine):
    SQLModel.metadata.create_all(engine)


def drop_all_tables(engine):
    SQLModel.metadata.drop_all(engine)
