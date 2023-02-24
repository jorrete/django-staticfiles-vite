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

# values
test = ${DJANGO_PATH}

install:
	test -d ${VENV_PATH} || python${PYTHON_VERSION} -m venv ${VENV_PATH}
	source ${VENV_PATH}/bin/activate
	pip install --upgrade pip
	pip install nodeenv
	nodeenv -p --node ${NODE_VERSION}
	pip install -e .[dev]
	mkdir ${EXAMPLE_PATH}/.django
	${DJANGO_PATH}/manage.py migrate

collectstatic:
	source ${VENV_PATH}/bin/activate
	${DJANGO_PATH}/manage.py collectstatic --clear --noinput --vite

dev:
	source ${VENV_PATH}/bin/activate
	export DJANGO_DEBUG=true
	${DJANGO_PATH}/manage.py runserver 0.0.0.0:${DJANGO_PORT} --vite=auto

dev-prod:
	source ${VENV_PATH}/bin/activate
	export DJANGO_DEBUG=false
	${DJANGO_PATH}/manage.py collectstatic --clear --noinput --vite --tests
	${DJANGO_PATH}/manage.py runserver 0.0.0.0:${DJANGO_PORT}

test:
	source ${VENV_PATH}/bin/activate
	${DJANGO_PATH}/manage.py test $(test)

test-debug:
	source ${VENV_PATH}/bin/activate
	export TESTING_BROWSER_DEBUG=true
	./${DJANGO_PATH}/manage.py test --failfast --keepdb  --verbosity 2 $(test)

black:
	black --preview ${MODULE_PATH} ${EXAMPLE_PATH}

isort:
	isort ${MODULE_PATH} ${EXAMPLE_PATH}

flake8:
	flake8 ${MODULE_PATH} ${EXAMPLE_PATH}

autoflake:
	autoflake --config .autoflake --verbose ${MODULE_PATH} ${EXAMPLE_PATH}

eslint:
	npx eslint --fix ${MODULE_PATH}/node/*.js

pre-commit:
	pre-commit run --all-files
