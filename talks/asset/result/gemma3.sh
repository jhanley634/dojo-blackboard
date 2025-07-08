#! /usr/bin/env bash

# This facilitates interactively pasting in several prompts for a single LLM response.

MODEL=${1:-gemma3:12b}
DIR=/tmp/k
TEMP=${DIR}/${MODEL}-prompt.txt
LOG=${DIR}/${MODEL}-prompts.txt

if [ "$MODEL" = deepseek ]
then
    MODEL=deepseek-coder-v2
fi

mkdir -p "${DIR}"
rm -f "${TEMP}"

bash -xc 'cat' > "${TEMP}"
printf '\n\n----\n\n\n' >> "${LOG}"
cat "${TEMP}" >> "${LOG}"
set -x
time ollama run "${MODEL}"  < "${TEMP}"
