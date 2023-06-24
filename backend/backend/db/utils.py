from sqlmodel import Session, create_engine, func, select, text
from backend.model import Item

from backend.utils import read_secret


def generate_engine(
    host: str, port: int, db: str, user: str, pw: str, schema: str = "curios", **kwargs
):
    connect_args = {"options": f"-csearch_path={schema}"}
    return create_engine(
        f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}",
        connect_args=connect_args,
        **kwargs,
    )


def add_single(v, session: Session):
    session.add(v)
    session.commit()
    return v


def add_many(vs, session: Session):
    session.add_all(vs)
    session.commit()
    return vs


def count(t, session: Session) -> int:
    return session.exec(select(func.count(t.id))).first()


def truncate(t, session: Session, cascade: bool = False):
    if cascade:
        stmt = text(f"TRUNCATE TABLE {t} CASCADE")
    else:
        stmt = text(f"TRUNCATE TABLE {t}")
    session.exec(stmt)
    session.commit()


def get_engine(**kwargs):
    host = read_secret("postgres_host")
    port = read_secret("postgres_port")
    db = read_secret("postgres_db")
    user = read_secret("postgres_user")
    pw = read_secret("postgres_password")
    schema = "curios"
    return generate_engine(host, port, db, user, pw, schema, **kwargs)
