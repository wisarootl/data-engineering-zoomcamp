lint:
	poetry run black .
	poetry run isort .
	poetry run ruff check .
	poetry run mypy .

cd:
	cd 01-docker-terraform/2_docker_sql