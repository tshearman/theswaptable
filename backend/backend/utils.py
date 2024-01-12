from fastapi import HTTPException
from sqlmodel import Session


def read_config(value):
    return read_from_file(f"/run/config/{value}")

def read_secret(secret):
    return read_from_file(f"/run/secrets/{secret}")

def read_from_file(filepath):
    with open(filepath, "r") as f:
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


def with_session(engine, commit: bool = False, **session_kwargs):
    def decorated(func):
        def inner(*args, **kwargs):
            with Session(engine, **session_kwargs) as session:
                response = func(*args, session, **kwargs)
                if commit:
                    session.commit()
                return response

        return inner

    return decorated


def or404session(engine, type_, commit: bool = False, **session_kwargs):
    def decorated(func):
        func_with_session = with_session(engine, commit, **session_kwargs)(func)
        return or404(type_)(func_with_session)

    return decorated
