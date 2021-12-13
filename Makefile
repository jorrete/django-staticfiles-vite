MODULE_PATH="django_staticfiles_vite"
EXAMPLE_PATH="example"
VENV_PATH=".venv"

development:
	python3 -m venv ${VENV_PATH}
	source ${VENV_PATH}/bin/activate
	pip install --upgrade pip
	pip install -e .[dev]
