black .
flake=$(flake8 . --count --max-complexity=15 --max-line-length=88 --statistics)
style=$(pydocstyle . --count)
if [[ "$flake" != 0 || "$style" != 0 ]]; then
    echo "flake errors: $flake"
    echo "doc style errors: $style"
    flake8 . --count --max-complexity=15 --max-line-length=88 --statistics
    pydocstyle .
    echo "press enter to continue"
    read
fi
