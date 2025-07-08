#! /usr/bin/env bash

set -e

trap ctrl_c SIGINT

ctrl_c() {
    echo Bye.
}

cd ../dojo-blackboard/
cd ../dojo-blackboard/talks/asset/result/

MODELS=(
    gemma3:12b
    olmo2:13b
    deepseek-coder-v2
    cogito:14b
    deepseek-r1:14b
    phi4
    qwen3:14b
    phi4-reasoning
    devstral
    magistral
)

echo "${MODELS[*]}"

for prompt in prompt-*.md
do
    title="${prompt#prompt-}"
    title="${title%.md}"

    for model in "${MODELS[@]}"
    do
        out="$model-$title.md"
        echo "$(date +'%Y-%m-%d %H:%M:%S')   $out"
        bash -c "/usr/bin/time gemma3.sh $model  2>&1"  < "$prompt"  > "$out"
    done
done
