FROM python:3.11
RUN mkdir /app 
RUN mkdir /app/backend
RUN mkdir /app/tests
COPY /backend/ /app/backend/
COPY /tests/ /app/tests/
COPY pyproject.toml /app
EXPOSE 8000
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:/app:/app/backend
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
CMD uvicorn app:app --host 0.0.0.0 --port 8000
