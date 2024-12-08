install:
	poetry install --no-root

build:
	poetry build

lint:
	poetry run flake8

dev:
	poetry run flask --app page_analyzer:app run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app