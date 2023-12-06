#!/bin/bash

black game/
style=`pydocstyle game/ --count`
flake=`flake8 game/ --max-complexity=15 --max-line-length=88 --count`
if [[ $flake != 0 || $style != 0 ]]; then
    echo "flake errors: $flake"
    echo "doc style errors: $style"
    flake8 game/ --count --max-complexity=15 --max-line-length=88 --statistics
    pydocstyle game/
    echo "press enter to continue"
    read
else
    exit 0
fi