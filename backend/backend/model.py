from datetime import datetime
from typing import List
import uuid
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import registry
from sqlalchemy.sql import func


reg = registry()


@reg.mapped_as_dataclass
class ItemType:
    __tablename__ = "dim_item_types"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    lookup_table: Mapped[str] = mapped_column(nullable=False)
    create_ts: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, default=datetime.now()
    )


@reg.mapped_as_dataclass
class User:
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)
    id: Mapped[str] = mapped_column(
        primary_key=True, default_factory=lambda: str(uuid.uuid4()), unique=True
    )
    create_ts: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, default=datetime.now()
    )


@reg.mapped_as_dataclass
class Item:
    __tablename__ = "items"
    type_id: Mapped[int] = mapped_column(ForeignKey("dim_item_types.id"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True, default=None)
    img_location: Mapped[str] = mapped_column(nullable=True, default=None)
    id: Mapped[str] = mapped_column(
        primary_key=True, default_factory=lambda: str(uuid.uuid4()), unique=True
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    create_ts: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, default=datetime.now()
    )


@reg.mapped_as_dataclass
class BookDetails:
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
    author: Mapped[str] = mapped_column(nullable=True, default=None)
    publisher: Mapped[str] = mapped_column(nullable=True, default=None)
    isbn: Mapped[str] = mapped_column(nullable=True, default=None)
    create_ts: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, default=datetime.now()
    )


@reg.mapped_as_dataclass
class Vote:
    __tablename__ = "votes"
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id: Mapped[str] = mapped_column(
        primary_key=True, default_factory=lambda: str(uuid.uuid4()), unique=True
    )
    create_ts: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, default=datetime.now()
    )
