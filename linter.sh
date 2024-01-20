#!/bin/bash

black m1wengine/
style=`pydocstyle m1wengine/ --count`
flake=`flake8 m1wengine/ --max-complexity=15 --max-line-length=88 --count`
if [[ $flake != 0 || $style != 0 ]]; then
    echo "flake errors: $flake"
    echo "doc style errors: $style"
    flake8 m1wengine/ --count --max-complexity=15 --max-line-length=88 --statistics
    pydocstyle m1wengine/
    echo "press enter to continue"
    read
else
    exit 0
fi