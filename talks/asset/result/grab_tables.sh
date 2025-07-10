#! /usr/bin/env bash

set -e

cd ../dojo-blackboard/
cd ../dojo-blackboard/talks/asset/result/

TEMP=/tmp/k/table
mkdir -p "$TEMP"

for output in *.md
do
    egrep '^\|'  "$output" |
        sed -e 's/  */ /g'  > "$TEMP/$output"
done
