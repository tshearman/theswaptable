clean:
	docker container prune -f
	docker image prune -f
	docker volume prune -f

build:
	docker compose build

up:
	docker compose up

pytest:
	docker compose run --rm api pytest -m "not external"

pytest/full:
	docker compose run --rm api pytest

down: 
	docker compose down

lint:
	black .

dev: build up down clean

test: build pytest down clean

test-full: build pytest/full down clean

t: test

tf: test-full

d: dev

l: lint
