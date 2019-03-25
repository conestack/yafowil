#!/bin/sh
if [ -x "$(which python)" ]; then
    ./py2/bin/python -m yafowil.tests.__init__
fi
if [ -x "$(which python3)" ]; then
    ./py3/bin/python -m yafowil.tests.__init__
fi
