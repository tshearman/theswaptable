from sqlmodel import create_engine, func, select, text

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


def is_successful(f):
    def f_star(*args, **kwargs):
        f(*args, **kwargs)
        return True

    return f_star


@is_successful
def add_single(item, session) -> None:
    session.add(item)
    session.commit()


@is_successful
def add_many(items, session) -> None:
    session.add_all(items)
    session.commit()


def count(t, session) -> int:
    return session.exec(select(func.count(t.id))).first()


def truncate(t, session, cascade=False):
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
