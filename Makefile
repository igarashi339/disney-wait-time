.PHONY: up
up:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down

.PHONY: build
build:
	docker-compose build --no-cache

.PHONY: delete-all
delete-all:
	docker-compose down --rmi all --volumes

.PHONY: fetch-sea
fetch-sea:
	docker-compose exec scraping python src/sea/main.py