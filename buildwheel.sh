#! /bin/sh
set -e;

python setup.py bdist_wheel > /dev/null;

LATEST=$(ls -t1 dist | head -n 1)

echo Built $LATEST

if [ $# -eq 1 ] && [ $1 = install ]; then
  pip install $LATEST
  echo Installed to dist-packages/
fi

./clearbuild.sh
