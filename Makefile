test:
	docker compose down && docker compose build && docker compose run api pytest && docker compose rm -f
