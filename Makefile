build:
	docker compose build

up:
	docker compose up -d --remove-orphans

stop:
	docker compose stop

down:
	docker compose down

test:
	docker compose exec -it backend /bin/sh -c "pytest . --reuse-db"

exec_backend:
	docker compose exec -it backend bash
