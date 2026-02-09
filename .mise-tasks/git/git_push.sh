#!/bin/bash
#MISE alias="push"
#MISE description="git add . + git commit -m 'update' + git push"

# This script is a QoL tool cause I'm lazy

git add .
git commit -m "update $(date '+%Y-%m-%d %H:%M:%S')"
git push