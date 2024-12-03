#! /usr/bin/env bash

which cloc  > /dev/null && exit 1  # already installed, nothing to do

set -e -x

if $(uname -s | grep -q Darwin); then
    brew install cloc
else
    sudo apt-get install -y cloc
fi
