#!/usr/bin/env bash
export PYTHONPATH=$PYTHONPATH:$PWD/src:$PWD/tests
python3 -m unittest discover -s tests
