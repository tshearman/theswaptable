test:
	docker compose build
	docker compose run --rm api pytest
	docker compose down
	docker container prune -f
	docker image prune -f
	docker volume prune -f

dev:
	docker compose build
	docker compose up
	docker compose down
	docker container prune -f
	docker image prune -f
	docker volume prune -f

t: test

d: dev