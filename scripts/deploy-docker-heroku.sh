#!/bin/bash

set -e

imagename=$1
appname=$2
echo "Setting up to deploy docker image "$imagename" to site servers (Heroku) "$appname""
docker tag "$imagename" registry.heroku.com/"$appname"/web
docker push registry.heroku.com/"$appname"/web
heroku container:release web --app "$appname"
