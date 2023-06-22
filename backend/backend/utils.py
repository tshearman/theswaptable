def read_secret(secret):
    file_name = f"/run/secrets/{secret}"
    with open(file_name, "r") as f:
        return f.readline()
