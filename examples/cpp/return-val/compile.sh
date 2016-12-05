#! /bin/sh

set -e

# $argv[1] is for_submission from cpp.pre_evaluate
# TODO: remove old files?

if [ $argv[1] = true ] ; then
    # make submission
    gcc main.o submitMain.cpp -I grader/include
else
    make testing
fi

exit 0