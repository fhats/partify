#! /bin/sh
# A quick script to package for PyPI
git pull origin
make
python setup.py sdist upload