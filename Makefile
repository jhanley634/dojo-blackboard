
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
	$(ACTIVATE) && pyright .
	$(ACTIVATE) && mypy $(STRICT) .

unit:
	$(ACTIVATE) && env SKIP_SLOW=1 python -m unittest $(VERBOSE) tests**/*_test.py
test: unit
	$(ACTIVATE) && pytest --cov --cov-report=term-missing

run:
	$(ACTIVATE) && fastapi dev src/bboard/main.py

# tutorial is at https://docs.beeware.org/en/latest/tutorial/tutorial-1.html
HELLOWORLD := src/beeware-tutorial/helloworld
BUILD := /tmp/dojo/helloworld/build

$(BUILD):
	mkdir -p $(BUILD)
	cd $(HELLOWORLD) && ln -s $(BUILD)

build: $(BUILD)
	$(ACTIVATE) && cd $(HELLOWORLD) && briefcase build && briefcase update
	# another relevant command would be: briefcase run iOS --update

install: $(HOME)/.venv/$(PROJECT)/bin/activate $(BUILD)
	$(ACTIVATE) && uv pip install --upgrade -r requirements.txt
	$(ACTIVATE) && pre-commit install

$(HOME)/.venv/$(PROJECT)/bin/activate:
	python -m venv $(HOME)/.venv/$(PROJECT)
	$(ACTIVATE) && pip install uv
	$(ACTIVATE) && uv venv $(HOME)/.venv/$(PROJECT) --python=3.12.7
	$(ACTIVATE) && which python && python --version

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

PANDOC := pandoc -o out/2024-09-24-trip-report.pdf 2024-09-24-trip-report.md
talk:
	docker run -v $$(pwd)/talks:/tmp pandoc  -c 'cd /tmp && ls -lR && $(PANDOC)'

CACHES := .mypy_cache/ .pyre/ .pytype/ .ruff_cache/ $(HELLOWORLD)/logs $(shell find . -name __pycache__)

clean:
	rm -rf $(CACHES) htmlcov/ $(HOME)/.venv/$(PROJECT) /tmp/blackboard.db

.PHONY: all lint unit test run build install coverage talk clean
