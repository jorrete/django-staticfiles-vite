MODULE_PATH="django_staticfiles_vite"
EXAMPLE_PATH="test_app"
VENV_PATH=".venv"

install:
	test -d ${VENV_PATH} || python3 -m venv ${VENV_PATH} || :
	source ${VENV_PATH}/bin/activate
	pip install --upgrade pip
	pip install -e .[dev]
	test -d ${VENV_PATH} || nodeenv -p || :
	cd ${EXAMPLE_PATH} && npm install

dev:
	source ${VENV_PATH}/bin/activate
	./${EXAMPLE_PATH}/django/manage.py runserver --vite=auto

test:
	source ${VENV_PATH}/bin/activate
	./${EXAMPLE_PATH}/django/manage.py test

debugpy:
	source ${VENV_PATH}/bin/activate
	./${EXAMPLE_PATH}/django/manage.py runvite &
	python -m debugpy --listen 5678 --wait-for-client ./${EXAMPLE_PATH}/django/manage.py runserver --noreload --nothreading --vite=manual

black:
	black ${MODULE_PATH}

flake8:
	flake8 ${MODULE_PATH}

prepare: black flake8
