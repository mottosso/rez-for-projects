#!/usr/bin/env bash

dp0="$( cd "$(dirname "$0")" ; pwd -P )"

# Install packages here
export REZ_LOCAL_PACKAGES_PATH=$dp0/../.packages

# Look for packages here
export REZ_PACKAGES_PATH=$dp0/../.packages

export PS1="$ "

export GITLAB_API_KEY=abc123
export FTRACK_API_KEY=abc123

alias re='rez env'
alias ri='rez build --install'

cat $dp0/banner.txt
