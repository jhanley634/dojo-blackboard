
PROJECT := dojo-blackboard
ACTIVATE := source $(HOME)/.venv/$(PROJECT)/bin/activate
SHELL := bash -u -e -o pipefail
PYTHONPATH := src:.

all:
	ls -l

STRICT = --strict --warn-unreachable --ignore-missing-imports --no-namespace-packages

ruff-check:
	$(ACTIVATE) && black . && isort . && ruff check
lint: ruff-check
	$(ACTIVATE) && mypy $(STRICT) .
	$(ACTIVATE) && pyright .

unit:
	$(ACTIVATE) && env SKIP_SLOW=1 python -m unittest $(VERBOSE) tests**/*_test.py
test: unit
	$(ACTIVATE) && pytest --cov --cov-report=term-missing

run:
	$(ACTIVATE) && fastapi dev src/bboard/main.py

install: $(HOME)/.venv/$(PROJECT)/bin/activate
	$(ACTIVATE) && pip install -r requirements.txt
	$(ACTIVATE) && pre-commit install

$(HOME)/.venv/$(PROJECT)/bin/activate:
	python -m venv $(HOME)/.venv/$(PROJECT)

SOURCES := $(shell find . -name '*.py')
EXCLUDE := '^(main|lifespan_mgmt|clock_[ps]ub)\.py$$'

coverage: htmlcov/index.html

htmlcov/index.html: $(SOURCES)
	$(ACTIVATE) && coverage erase
	$(ACTIVATE) && coverage run -m unittest tests**/*_test.py
	$(ACTIVATE) && coverage html
	$(ACTIVATE) && coverage report
	ls htmlcov/z_*_py.html | sed -e 's;htmlcov/z_................_;;' -e 's;_py\.html$$;.py;' | sort > /tmp/tested
	find . -name '*.py' | sed -e 's;.*/;;' | egrep -v $(EXCLUDE) | sort | diff -u /tmp/tested -

clean:
	rm -rf htmlcov/ $(HOME)/.venv/$(PROJECT) /tmp/blackboard.db

.PHONY: all lint unit test run install coverage clean
