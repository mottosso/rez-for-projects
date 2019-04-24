#!/usr/bin/env bash
dp0=$(dirname ${BASH_SOURCE[0]})

# Install packages here
export REZ_LOCAL_PACKAGES_PATH=$(realpath $dp0/../local_packages_path)
export REZ_RELEASE_PACKAGES_PATH=$(realpath $dp0/../release_packages_path)

# Look for packages here
export REZ_PACKAGES_PATH=$REZ_PACKAGES_PATH:$REZ_LOCAL_PACKAGES_PATH:$REZ_RELEASE_PACKAGES_PATH

export PS1="(rez) $ "

export GITLAB_API_KEY=abc123
export FTRACK_API_KEY=abc123

alias re='rez env'
alias ri='rez build --install'

cat $dp0/banner.txt
