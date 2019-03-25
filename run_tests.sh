#!/bin/sh
set -e
TEST="bin/python -m yafowil.tests.__init__"

clear

if [ -x "$(which python)" ]; then
    ./py2/$TEST
fi

echo ""

if [ -x "$(which python3)" ]; then
    ./py3/$TEST
fi
