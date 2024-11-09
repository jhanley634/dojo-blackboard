
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

unit: count
	$(ACTIVATE) && env PYTHONPATH=$(PYTHONPATH) SKIP_SLOW=1 python -m unittest $(VERBOSE) {src/count/,}tests**/*_test.py
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

FIND_SOURCES := find . -name '*.py' | grep -v '/src/beeware-tutorial/helloworld/'
SOURCES := $(shell $(FIND_SOURCES))
EXCLUDE := '^(main|lifespan_mgmt|clock_[ps]ub)\.py$$'

coverage: htmlcov/index.html

htmlcov/index.html: $(SOURCES)
	$(ACTIVATE) && coverage erase
	$(ACTIVATE) && coverage run -m unittest {src/count/,}tests**/*_test.py
	$(ACTIVATE) && coverage html
	$(ACTIVATE) && coverage report
	ls htmlcov/z_*_py.html | sed -e 's;htmlcov/z_................_;;' -e 's;_py\.html$$;.py;' | sort > /tmp/tested
	$(FIND_SOURCES)  | sed -e 's;.*/;;' | egrep -v $(EXCLUDE) | sort | diff -u /tmp/tested -

REPOS := /tmp/repos
$(REPOS):
	rm -rf $(REPOS)
	mkdir -p $(REPOS)
	cd $(REPOS) && git clone https://github.com/ggerganov/llama.cpp
	cd $(REPOS) && git clone https://github.com/paslandau/docker-php-tutorial
	rm $(REPOS)/docker-php-tutorial/resources/views/home.blade.php

FIND := find $(REPOS) -type f -name '*.cpp' -o -name '*.php'
count: $(REPOS)
	$(FIND) | sort | xargs cloc  # brew install cloc, or apt install cloc

PANDOC := pandoc -o out/2024-09-24-trip-report.pdf 2024-09-24-trip-report.md
talk:
	docker run -v $$(pwd)/talks:/tmp pandoc  -c 'cd /tmp && ls -lR && $(PANDOC)'

docker:
	docker build --tag $(PROJECT) .
	docker run -it --rm $(PROJECT)

CACHES = .mypy_cache/ .pyre/ .pytype/ .ruff_cache/ $(HELLOWORLD)/logs $(shell find . -name __pycache__)

clean:
	rm -rf $(HELLOWORLD)/build
	rm -rf $(CACHES) htmlcov/ $(HOME)/.venv/$(PROJECT) $(REPOS) /tmp/blackboard.db

.PHONY: all lint unit test run build install coverage count talk docker clean
