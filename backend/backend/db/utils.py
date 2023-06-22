from sqlmodel import Session, create_engine


def generate_engine(
    host: str, port: int, db: str, user: str, pw: str, schema: str = "curios"
):
    connect_args = {"options": f"-csearch_path={schema}"}
    return create_engine(
        f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}",
        connect_args=connect_args,
    )


def is_successful(f):
    def f_star(*args, **kwargs):
        try:
            f(*args, **kwargs)
            return True
        except:
            return False

    return f_star


@is_successful
def add_single(item, engine):
    with Session(engine) as session:
        session.add(item)
        session.commit()


@is_successful
def add_many(items, engine):
    with Session(engine) as session:
        session.add_all(items)
        session.commit()
