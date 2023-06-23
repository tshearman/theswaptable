from sqlmodel import Session, create_engine, func, select, text


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
def add_single(item, engine) -> None:
    with Session(engine) as session:
        session.add(item)
        session.commit()


@is_successful
def add_many(items, engine) -> None:
    with Session(engine) as session:
        session.add_all(items)
        session.commit()


def count(t, engine) -> int:
    with Session(engine) as session:
        return session.exec(select(func.count(t.id))).first()


def truncate(t, engine, cascade=False):
    with Session(engine) as session:
        if cascade:
            stmt = text(f"TRUNCATE TABLE {t} CASCADE")
        else:
            stmt = text(f"TRUNCATE TABLE {t}")
        session.exec(stmt)
        session.commit()
