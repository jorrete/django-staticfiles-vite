MODULE_PATH="django_staticfiles_vite"
EXAMPLE_PATH="test_app"
VENV_PATH=".venv"

install:
	python3 -m venv ${VENV_PATH}
	source ${VENV_PATH}/bin/activate
	pip install --upgrade pip
	pip install -e .[dev]
	nodeenv -p
	cd ${EXAMPLE_PATH}
	npm install

dev:
	cd ${EXAMPLE_PATH}/django && ./manage.py runserver --vite

test:
	cd ${EXAMPLE_PATH}/django && ./manage.py test

black:
	black ${MODULE_PATH}

flake8:
	flake8 ${MODULE_PATH}

prepare: black flake8
