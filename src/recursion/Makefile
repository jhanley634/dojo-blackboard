
REC := /tmp/recursion

DIR := $(shell pwd)

all:
	cd /tmp && ls -l

setup: \
  $(REC)/py3.14 \
  $(REC)/py3.13 \
  $(REC)/py3.12 \
  $(REC)/py3.11 \
  $(REC)/py3.10 \
  $(REC)/py3.9 \
  $(REC)/py3.8 \

GREP := awk '/^Using / {print "\t\t\t", $$0}'

py%:
	@mkdir -p $@
	cd $@ && uv venv --managed-python --python $(shell basename $*) 2>&1 | $(GREP)
	cd $@ && source .venv/bin/activate && python $(DIR)/count.py

clean:
	rm -rf $(REC)
