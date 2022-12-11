.PHONY: *
.ONESHELL:
.SILENT:
NODE_VERSION=18.12.1
PYTHON_VERSION=3.9
MODULE_PATH=django_staticfiles_vite
EXAMPLE_PATH=test_app
DJANGO_PATH=${EXAMPLE_PATH}/django
VENV_PATH=.venv
DJANGO_PORT=8000

install:
	test -d ${VENV_PATH} || python${PYTHON_VERSION} -m venv ${VENV_PATH}
	source ${VENV_PATH}/bin/activate
	pip install --upgrade pip
	pip install nodeenv
	nodeenv -p --node ${NODE_VERSION}
	pip install -e .[dev]
	mkdir ${EXAMPLE_PATH}/.django
	${DJANGO_PATH}/manage.py migrate

dev:
	source ${VENV_PATH}/bin/activate
	${DJANGO_PATH}/manage.py runserver 0.0.0.0:${DJANGO_PORT} --vite=auto

collectstatic:
	source ${VENV_PATH}/bin/activate
	${DJANGO_PATH}/manage.py collectstatic --clear --noinput --vite

dev-prod:
	source ${VENV_PATH}/bin/activate
	export DJANGO_DEBUG=false
	${DJANGO_PATH}/manage.py collectstatic --clear --noinput --vite
	${DJANGO_PATH}/manage.py runserver 0.0.0.0:${DJANGO_PORT}

test:
	source ${VENV_PATH}/bin/activate
	${DJANGO_PATH}/manage.py test ${DJANGO_PATH}

test-browser:
	source ${VENV_PATH}/bin/activate
	export DJANGO_TEST_HEADLESS=false
	./${DJANGO_PATH}/manage.py migrate test

black:
	black --preview ${MODULE_PATH} ${EXAMPLE_PATH}

isort:
	isort ${MODULE_PATH} ${EXAMPLE_PATH}

flake8:
	flake8 ${MODULE_PATH} ${EXAMPLE_PATH}

autoflake:
	autoflake --config .autoflake --verbose ${MODULE_PATH} ${EXAMPLE_PATH}

pre-commit:
	pre-commit run --all-files
