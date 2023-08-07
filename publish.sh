#!/bin/bash

comment="$1"
git add .
git commit -m "$comment"
git push
rm -rf build
rm -rf dist
python setup.py sdist
twine upload dist/*