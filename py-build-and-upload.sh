#!/usr/bin/env bash

py="/usr/bin/env python3"

rm -rf dist build

$py clean --all
$py setup.py sdist bdist_wheel
twine upload dist/*