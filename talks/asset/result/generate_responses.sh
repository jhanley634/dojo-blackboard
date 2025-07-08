#! /usr/bin/env bash

set -e

trap ctrl_c SIGINT

ctrl_c() {
    echo " Bye."
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
    phi4-reasoning
    devstral
)

echo "${MODELS[*]}"

for prompt in prompt-*.md
do
    title="${prompt#prompt-}"
    title="${title%.md}"

    for model in "${MODELS[@]}"
    do
        out="$model-$title.md"
        if [ -r "$out" ]
        then
            ls -l "$out"
        else
            echo "$(date +'%Y-%m-%d %H:%M:%S')   $out"
            (echo "-*- org -*-";
             echo;
             gemma3.sh "$model"  < "$prompt"  2>&1 |
                 egrep --line-buffered -v '^\xe2\xa0' |
                 sed -u -e 's/\x1b[[][?]*[0-9;]*[a-zA-Z]//g') |
            cat  > "$out"
            # The sed suppresses any "progress" ANSI escapes.
            sleep 1  # A double CTRL/C will hit this command.
        fi
    done
done
