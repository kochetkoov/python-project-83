install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer.app:app run

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	uv run flake8

check:
	ruff check --fix --select I