#!/bin/sh
./$1/bin/coverage run --source src/yafowil src/yafowil/tests/__init__.py
./$1/bin/coverage report
./$1/bin/coverage html
