
REC := /tmp/recursion

all:
	cd /tmp && ls -l

setup: \
  $(REC)/py3.9 \
  $(REC)/py3.10 \
  $(REC)/py3.11 \
  $(REC)/py3.12 \

py%:
	mkdir -p $@
	cd $@ && uv venv --managed-python --python $(shell basename $*)
	cd $@ && source .venv/bin/activate && python --version

clean:
	rm -rf $(REC)
