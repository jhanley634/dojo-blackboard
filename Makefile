
PROJECT := dojo-blackboard
ACTIVATE := source $(HOME)/.venv/$(PROJECT)/bin/activate
SHELL := bash -u -e -o pipefail

all:
	ls -l

STRICT = --strict --warn-unreachable --ignore-missing-imports --no-namespace-packages

lint:
	$(ACTIVATE) && black . && isort . && ruff check
	$(ACTIVATE) && pyright .
	$(ACTIVATE) && mypy $(STRICT) .

test:
	$(ACTIVATE) && python -m unittest tests**/*_test.py
	$(ACTIVATE) && pytest --cov --cov-report=term-missing

run:
	$(ACTIVATE) && fastapi dev src/bboard/main.py

install: $(HOME)/.venv/$(PROJECT)/bin/activate
	$(ACTIVATE) && pip install -r requirements.txt
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pre-commit install

$(HOME)/.venv/$(PROJECT)/bin/activate:
	python -m venv $(HOME)/.venv/$(PROJECT)

SOURCES := **/*.py

coverage: htmlcov/index.html

htmlcov/index.html: $(SOURCES)
	$(ACTIVATE) && coverage erase
	$(ACTIVATE) && coverage run -m unittest tests**/*_test.py
	$(ACTIVATE) && coverage html
	$(ACTIVATE) && coverage report
	ls htmlcov/z_*_py.html | sed -e 's;htmlcov/z_................_;;' -e 's;_py\.html$$;.py;' | sort > /tmp/tested
	find . -name '*.py' | sed -e 's;.*/;;' | egrep -v '^main\.py$$' | sort | diff -u /tmp/tested -

clean:
	rm -rf htmlcov/ $(HOME)/.venv/$(PROJECT)

.PHONY: all lint test run install coverage clean
