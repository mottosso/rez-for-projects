#!/usr/bin/env bash
dp0="$( cd "$(dirname "$0")" ; pwd -P )"
source $dp0/.rez/env.sh
python $dp0/.rez/build_all.py $*
