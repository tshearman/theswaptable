FROM python:3.11
RUN mkdir /app 
COPY /backend/ /app/
COPY pyproject.toml /app
EXPOSE 8000
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:/app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
CMD uvicorn app:app --host 0.0.0.0 --port 8000
