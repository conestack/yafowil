#!/bin/bash

DOMAIN="yafowil"
BASE_PATH=src/yafowil
LOCALES_PATH=src/yafowil/i18n/locales

cd $LOCALES_PATH
mkdir -p $1/LC_MESSAGES
msginit -i $DOMAIN.pot -o $1/LC_MESSAGES/$DOMAIN.po -l $1
