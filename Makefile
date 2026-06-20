.PHONY: requirements messages

DJANGO_MANAGE_PY = src/manage.py

requirements:
	poetry export -f requirements.txt --without-hashes --output requirements.txt
	poetry export -f requirements.txt --without-hashes --with dev --output requirements-dev.txt

messages:
	poetry run python $(DJANGO_MANAGE_PY) makemessages -l de --ignore=venv --ignore=src/static --ignore=src/media --ignore=src/node_modules --no-obsolete --add-location file