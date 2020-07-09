#!/bin/bash

set -e

echo "Jenkins will push the code to the master branch"
git config --add remote.origin.fetch +refs/heads/master:refs/remotes/origin/master
git checkout test
git pull
git checkout master
git pull origin master
git merge --no-ff --no-commit test
git status
git commit -m 'merge test branch'
git push origin master