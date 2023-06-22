from sqlalchemy import create_engine


def read_secret(secret):
    file_name = f"/run/secrets/{secret}"
    with open(file_name, "r") as f:
        return f.readline()


def generate_connection():
    host = read_secret("postgres_host")
    port = read_secret("postgres_port")
    db = read_secret("postgres_db")
    user = read_secret("postgres_user")
    password = read_secret("postgres_password")
    connect_args = {"options": "-csearch_path=curios"}
    return create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}",
        connect_args=connect_args,
    )
