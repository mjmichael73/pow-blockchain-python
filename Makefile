# Makefile for Proof of Work Blockchain Project

.PHONY: help build up down restart test test-docker lint format clean

help:
	@echo "Available commands:"
	@echo "  build         - Build Docker images"
	@echo "  up            - Start services in background"
	@echo "  down          - Stop and remove containers"
	@echo "  restart       - Restart all services"
	@echo "  test          - Run tests inside a Docker container"
	@echo "  lint          - Check code style inside a Docker container"
	@echo "  format        - Auto-format code inside a Docker container"
	@echo "  clean         - Remove temporary files and caches"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart: down up

test:
	docker compose run --rm blockchain-node pytest tests/

lint:
	docker compose run --rm blockchain-node flake8 .
	docker compose run --rm blockchain-node black --check .

format:
	docker compose run --rm blockchain-node black .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .venv
