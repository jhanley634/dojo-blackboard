
REC := /tmp/recursion
DIR := $(shell pwd)
SHELL := bash

all:
	cd /tmp && ls -l && echo && ulimit -s

measure: \
  $(REC)/py3.14 \
  $(REC)/py3.13 \
  $(REC)/py3.12 \
  $(REC)/py3.11 \
  $(REC)/py3.10 \
  $(REC)/py3.9 \
  $(REC)/py3.8 \

measure3.10: \
  $(REC)/py3.10 \
  $(REC)/py3.9 \
  $(REC)/py3.8 \

ACTIVATE := source .venv/bin/activate

py%:
	@mkdir -p $@
	@cd $@ && uv venv -q --managed-python --python $(shell basename $*)
	@cd $@ && $(ACTIVATE) && uv pip -q install polars psutil
	@cd $@ && $(ACTIVATE) && python $(DIR)/count.py

clean:
	rm -rf $(REC)
