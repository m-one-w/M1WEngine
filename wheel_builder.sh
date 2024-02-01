#!/bin/bash

rm -r build/ dist/
python setup.py bdist_wheel
pip install . --force-reinstall