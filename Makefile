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

.PHONY: fetch-and-store-sea
fetch-and-store-sea:
	docker-compose exec -T scraping python src/sea/main.py