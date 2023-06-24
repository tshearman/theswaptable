from sqlmodel import Session
from fastapi import HTTPException


def read_secret(secret):
    file_name = f"/run/secrets/{secret}"
    with open(file_name, "r") as f:
        return f.readline()


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


def with_session(engine, **kwargs):
    def decorated(func):
        def inner(*args, **kwargs):
            with Session(engine, **kwargs) as session:
                response = func(*args, **kwargs, session=session)
                return response

        return inner

    return decorated
