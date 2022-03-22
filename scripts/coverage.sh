#!/bin/bash

function run_coverage {
    local target=$1

    if [ -e "$target" ]; then
        ./$target/bin/coverage run --source src/yafowil src/yafowil/tests/__init__.py
        ./$target/bin/coverage report
    else
        echo "Target $target not found."
    fi
}

run_coverage py2
run_coverage py3
run_coverage pypy3
