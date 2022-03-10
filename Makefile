# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

# venv is a shortcut target
venv: $(VENV)/bin/activate

run:
	$(VENV)/bin/python manage.py runserver

test: venv
	.$(VENV)/bin/activate; pytest

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

env:
	python3 -m venv $(VENV)

build: env install-dependencies setup-project
	echo "Build Completed!"

install-dependencies:
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

setup-project:
	$(VENV)/bin/python manage.py makemigrations
	$(VENV)/bin/python manage.py migrate
	$(VENV)/bin/python manage.py loaddata usagetypes.json

.PHONY: all venv run clean env install-dependencies setup-project build