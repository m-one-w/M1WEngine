#!/bin/bash

path="."

black $path
style=`pydocstyle $path --count`
flake=`flake8 $path --extend-ignore=F811 --max-complexity=15 --max-line-length=88 --count`
if [[ $flake != 0 || $style != 0 ]]; then
    echo "flake errors: $flake"
    echo "doc style errors: $style"
    flake8 $path --count --extend-ignore=F811 --max-complexity=15 --max-line-length=88 --statistics
    pydocstyle $path
    echo "press enter to continue"
    read
else
    exit 0
fi