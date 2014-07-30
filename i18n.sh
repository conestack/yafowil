#!/bin/bash

DOMAIN="yafowil"
BASE_PATH=src/yafowil
LOCALES_PATH=src/yafowil/i18n/locales

# extract messages
pot-create $BASE_PATH -o $LOCALES_PATH/$DOMAIN.pot

# update translations
for po in $LOCALES_PATH/*/LC_MESSAGES/$DOMAIN.po; do
    msgmerge $po $LOCALES_PATH/$DOMAIN.pot
done

# compile catalogs
for po in $LOCALES_PATH/*/LC_MESSAGES/*.po; do
    msgfmt $po
done
