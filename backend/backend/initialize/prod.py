from db.utils import generate_engine
from model import initialize_tables
from utils import read_secret


def get_engine():
    host = read_secret("postgres_host")
    port = read_secret("postgres_port")
    db = read_secret("postgres_db")
    user = read_secret("postgres_user")
    pw = read_secret("postgres_password")
    schema = "curios"
    return generate_engine(host, port, db, user, pw, schema)


def init():
    initialize_tables(get_engine())
