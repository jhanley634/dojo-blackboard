
PROJECT := dojo-blackboard
ACTIVATE := source .venv/bin/activate
SHELL := bash -u -e -o pipefail
PYTHONPATH := src:.
ENV := env PYTHONPATH=$(PYTHONPATH)
# Once we used this, but no more.
ANCIENT_VENV := $(HOME)/.venv/$(PROJECT)

all:
	ls -l

STRICT = --strict --warn-unreachable --ignore-missing-imports --no-namespace-packages

ruff-check:
	$(ACTIVATE) && black . && isort . && ruff check
lint: ruff-check
	$(ACTIVATE) && pyright .
	$(ACTIVATE) && mypy $(STRICT) .

unit: count
	$(ACTIVATE) && $(ENV) SKIP_SLOW=1 python -m unittest $(VERBOSE) {src/count/,}tests**/*_test.py
test: unit
	$(ACTIVATE) && $(ENV) pytest --cov --cov-report=term-missing

# specify HOST=0.0.0.0 when running within a container, so docker can forward requests
HOST := localhost

run:
	$(ACTIVATE) && $(ENV) fastapi dev --host $(HOST) src/bboard/main.py

install: .venv/bin/activate
	$(ACTIVATE) && uv pip install --upgrade -r requirements.txt
	$(ACTIVATE) && pre-commit install

# The basemap package does not yet work with Python 3.13.
CHECK_INTERPRETER := -c 'import sys; v = sys.version_info; assert v.major == 3; assert v.minor <= 12, v.minor'

.venv/bin/activate:
	python -m venv .venv/
	$(ACTIVATE) && python -m pip install uv
	$(ACTIVATE) && which python && python --version && which uv
	$(ACTIVATE) && uv venv --python=3.12.7
	$(ACTIVATE) && which python && python --version
	$(ACTIVATE) && python -m ensurepip
	$(ACTIVATE) && python -m pip install uv
	$(ACTIVATE) && ls -la .venv/bin/
	$(ACTIVATE) && uv pip list

FIND_SOURCES := find . -name '*.py' | egrep -v '/.venv/'
SOURCES := $(shell $(FIND_SOURCES))
EXCLUDE := '^(main|lifespan_mgmt|clock_[ps]ub)\.py$$'

coverage: htmlcov/index.html

htmlcov/index.html: $(SOURCES)
	$(ACTIVATE) && coverage erase
	$(ACTIVATE) && $(ENV) coverage run -m unittest {src/count/,}tests**/*_test.py
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
	cd $(REPOS)/llama.cpp && git checkout --quiet b4160  # nothing special, it's just frozen

FIND := find $(REPOS) -type f -name '*.cpp' -o -name '*.php'
count: $(REPOS)
	which cloc  > /dev/null || src/bin/install-cloc.sh
	$(FIND) | sort | xargs cloc | wc -l

PANDOC := pandoc -o out/2024-09-24-trip-report.pdf 2024-09-24-trip-report.md
talk:
	docker run -v $$(pwd)/talks:/tmp pandoc  -c 'cd /tmp && ls -lR && $(PANDOC)'

CONTAINER_NAME = $(shell docker container ls -a | awk 'NR==2 {print $$12}')
CREDS := dojo-secrets/api-keys.txt

docker-build: clean-cache
	docker buildx build --tag $(PROJECT) .

docker-run:
	docker run -p 8000:8000 -it $(PROJECT)

CACHES = .mypy_cache/ .pyre/ .pytype/ .ruff_cache/ $(shell find . -name __pycache__)

clean-cache:
	rm -rf $(CACHES)

clean: clean-cache
	rm -rf htmlcov/ $(ANCIENT_VENV) .venv/ $(REPOS) /tmp/blackboard.db

.PHONY: all lint unit test run install coverage count talk docker clean
