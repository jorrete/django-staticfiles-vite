MODULE_PATH=django_staticfiles_vite
EXAMPLE_PATH=test_app
VENV_PATH=.venv

install:
	test -d ${VENV_PATH} || python3.9 -m venv ${VENV_PATH} || :
	source ${VENV_PATH}/bin/activate && pip install --upgrade pip
	source ${VENV_PATH}/bin/activate && pip install -e .[dev]
	source ${VENV_PATH}/bin/activate && test -d ${VENV_PATH} || nodeenv -p || :
	test -d ${EXAMPLE_PATH}/.django || mkdir ${EXAMPLE_PATH}/.django
	source ${VENV_PATH}/bin/activate && ./${EXAMPLE_PATH}/django/manage.py migrate
	cd ${EXAMPLE_PATH} && npm install
	# cd vite && npm install
	source ${VENV_PATH}/bin/activate && playwright install

dev:
	source ${VENV_PATH}/bin/activate && ./${EXAMPLE_PATH}/django/manage.py runserver --vite=auto

collectstatic:
	source ${VENV_PATH}/bin/activate && ./${EXAMPLE_PATH}/django/manage.py collectstatic --clear --noinput --vite

dev-prod:
	source ${VENV_PATH}/bin/activate && DJANGO_DEBUG=false ./${EXAMPLE_PATH}/django/manage.py collectstatic --clear --noinput --vite
	source ${VENV_PATH}/bin/activate && DJANGO_DEBUG=false ./${EXAMPLE_PATH}/django/manage.py runserver

test:
	source ${VENV_PATH}/bin/activate && cd ./${EXAMPLE_PATH}/django && ./manage.py test

test-browser:
	source ${VENV_PATH}/bin/activate && cd ./${EXAMPLE_PATH}/django && DJANGO_TEST_HEADLESS=false ./manage.py test

debugpy:
	source ${VENV_PATH}/bin/activate &&
	./${EXAMPLE_PATH}/django/manage.py runvite &
	python -m debugpy --listen 5678 --wait-for-client ./${EXAMPLE_PATH}/django/manage.py runserver --noreload --nothreading --vite=manual

black:
	black --preview ./${EXAMPLE_PATH}/django

isort:
	isort ./${EXAMPLE_PATH}/django

flake8:
	flake8 ./${EXAMPLE_PATH}/django

autoflake:
	autoflake --config .autoflake --verbose ./${EXAMPLE_PATH}/django

pre-commit:
	pre-commit run --all-files
