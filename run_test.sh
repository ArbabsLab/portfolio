#!/bin/bash

echo "Testing"
$PWD/python3-virtualenv/bin/python3 -m unittest discover -v tests/
echo "Testing Concluded"