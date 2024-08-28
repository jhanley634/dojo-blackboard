
PROJECT := dojo-blackboard
ACTIVATE := source $(HOME)/.venv/$(PROJECT)/bin/activate
SHELL := bash -u -e -o pipefail

all:
	ls -l

STRICT = --strict --warn-unreachable --ignore-missing-imports --no-namespace-packages

lint:
	$(ACTIVATE) && black . && isort . && ruff check
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

clean:
	rm -rf $(HOME)/.venv/$(PROJECT)

.PHONY: all lint test run install clean
