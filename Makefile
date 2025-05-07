.PHONY: build up down logs shell

build:
	podman-compose build

up:
	podman-compose up -d

down:
	podman-compose down

logs:
	podman-compose logs -f app

shell:
	podman-compose exec app /bin/bash