#! /bin/sh
set -e;

./clearbuild.sh

python3 setup.py bdist_wheel;
