#!/bin/sh
# This script generates the po/nautilus-hide.pot file
FILEPATH="$(readlink -f "$0")"
DIR="$(dirname "$FILEPATH")"
cd "$DIR"
xgettext --package-name=nautilus-hide --package-version=0.1.0 -cTRANSLATORS \
         "extension/nautilus-hide.py" -o "po/nautilus-hide.pot"
