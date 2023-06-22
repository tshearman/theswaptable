from backend.db.utils import generate_engine


def read_secret(secret):
    file_name = f"/run/secrets/{secret}"
    with open(file_name, "r") as f:
        return f.readline()


def get_engine():
    host = read_secret("postgres_host")
    port = read_secret("postgres_port")
    db = read_secret("postgres_db")
    user = read_secret("postgres_user")
    pw = read_secret("postgres_password")
    schema = "curios"
    return generate_engine(host, port, db, user, pw, schema, echo=True)
