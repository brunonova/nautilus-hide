#!/bin/sh
# This script generates the po/nautilus-hide.pot file
FILEPATH="$(readlink -f "$0")"
DIR="$(dirname "$FILEPATH")"
cd "$DIR"
xgettext --package-name=nautilus-hide \
         --package-version=0.2.1 \
         --copyright-holder='Bruno Nova <brunomb.nova@gmail.com>' \
         --msgid-bugs-address='https://github.com/brunonova/nautilus-hide/issues' \
         -cTRANSLATORS \
         -s -o "po/nautilus-hide.pot" \
         "extension/nautilus-hide.py"
