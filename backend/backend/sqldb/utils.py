from datetime import datetime

from fastapi import HTTPException
from pydantic import UUID4
from sqlmodel import Session, create_engine, func as f, select, text

from backend.utils import read_config, read_secret


def all_(t):
    def decorator(func):
        def inner(
            session: Session,
            offset: int | None = None,
            limit: int | None = None,
            **kwargs,
        ) -> list[t]:
            where = func(**kwargs)
            query = select(t).where(where)
            if offset is not None:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)
            return session.exec(query).all()

        return inner

    return decorator


def first(t):
    def decorated(func):
        def inner(session: Session, **kwargs) -> t | None:
            where = func(**kwargs)
            query = select(t).where(where)
            return session.exec(query).first()

        return inner

    return decorated


def count(t):
    def decorated(func):
        def inner(session: Session, **kwargs) -> int:
            where = func(**kwargs)
            query = select(f.count(t.id)).where(where)
            return session.exec(query).first()

        return inner

    return decorated


def truncate(t, session: Session, cascade: bool = False):
    if cascade:
        stmt = text(f"TRUNCATE TABLE {t.__tablename__} CASCADE")
    else:
        stmt = text(f"TRUNCATE TABLE {t.__tablename__}")
    session.exec(stmt)
    session.commit()


def create(t):
    def inner(session: Session, value: t) -> t:
        session.add(value)
        session.commit()
        return value

    return inner


def update(t, read):
    def inner(session: Session, *, id: UUID4, **kwargs) -> t:
        value = read(session, id=id)
        assert value is not None
        for k, v in kwargs.items():
            setattr(value, k, v)
        value.update_ts = datetime.now()
        session.add(value)
        session.commit()
        session.refresh(value)
        return value

    return inner


def delete(t, read):
    def inner(session: Session, *, id: UUID4) -> t:
        value = read(session, id=id)
        session.delete(value)
        session.commit()
        return value

    return inner


def generate_engine(
    host: str, port: int, db: str, user: str, pw: str, schema: str, **kwargs
):
    connect_args = {"options": f"-csearch_path={schema}"}
    return create_engine(
        f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}",
        connect_args=connect_args,
        **kwargs,
    )


def get_engine(**kwargs):
    host = read_config("postgres_host")
    port = read_config("postgres_port")
    db = read_config("postgres_db")
    user = read_secret("postgres_user")
    pw = read_secret("postgres_password")
    schema = read_config("postgres_schema")
    return generate_engine(host, port, db, user, pw, schema, **kwargs)


def or404(type_):
    def decorated(func):
        def inner(*args, **kwargs):
            response = func(*args, **kwargs)
            if response is None:
                detail = f"{type_.capitalize()} not found."
                raise HTTPException(status_code=404, detail=detail)
            return response

        return inner

    return decorated


def with_session(engine, commit: bool = False, **session_kwargs):
    def decorated(func):
        def inner(*args, **kwargs):
            with Session(engine, **session_kwargs) as session:
                response = func(*args, session, **kwargs)
                if commit:
                    session.commit()
                return response

        return inner

    return decorated


def or404session(engine, type_, commit: bool = False, **session_kwargs):
    def decorated(func):
        func_with_session = with_session(engine, commit, **session_kwargs)(func)
        return or404(type_)(func_with_session)

    return decorated
