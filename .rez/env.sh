#!/usr/bin/env bash
dp0=$(dirname ${BASH_SOURCE[0]})

# Install packages here
export REZ_RELEASE_PACKAGES_PATH=$(realpath $dp0/../packages)
export REZ_CONFIG_FILE=$(realpath $dp0/../rezconfig.py)

export PS1="(rez) $ "

export GITLAB_API_KEY=abc123
export FTRACK_API_KEY=abc123

alias re='rez env'
alias ri='rez build --install'

cat $dp0/banner.txt
