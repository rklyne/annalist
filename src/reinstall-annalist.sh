#!/usr/bin/env bash

echo "Reinstrall Annalist software from current source tree"
echo ""

pip uninstall annalist
python setup.py clean --all
python setup.py build
python setup.py install
annalist-manager runtests

# End.
