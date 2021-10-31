#!/bin/bash

if [ -x "$(which python)" ]; then
    rm -r py2

    virtualenv --clear --no-site-packages -p python py2

    ./py2/bin/pip install coverage
    ./py2/bin/pip install https://github.com/conestack/node/archive/master.zip
    ./py2/bin/pip install -e .[test]
fi
if [ -x "$(which python3)" ]; then
    rm -r py3

    virtualenv --clear --no-site-packages -p python3 py3

    ./py3/bin/pip install coverage
    ./py3/bin/pip install https://github.com/conestack/node/archive/master.zip
    ./py3/bin/pip install -e .[test]
fi
