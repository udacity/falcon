#! /bin/sh
set -e;

main() {
    rm -rf build;
    rm -rf dist;
    rm -rf .cache;
    rm -rf .eggs;
    rm -rf falcon.egg-info;
    rm -rf __pycache__;
    find . -name *.pyc -exec rm {} \;
}

main > /dev/null;
