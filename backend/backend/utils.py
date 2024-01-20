def read_config(value: str, dir_: str = "/run/config"):
    return read_from_file(f"{dir_}/{value}")


def read_secret(secret: str, dir_: str = "/run/secrets"):
    return read_from_file(f"{dir_}/{secret}")


def read_from_file(filepath):
    with open(filepath, "r") as f:
        return f.readline()


def get_google_search_app():
    search_app = read_config("google_search_app")
    token = read_secret("google_search_token")
    return search_app, token
