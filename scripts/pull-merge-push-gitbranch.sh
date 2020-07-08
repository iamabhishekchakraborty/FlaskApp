#!/bin/bash

set -e

echo "Jenkins will push the code to the master branch"
git checkout test
git pull
git checkout master
git pull
git merge --no-ff --no-commit test
git status
git commit -m 'merge test branch'
git push