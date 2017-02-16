#!/bin/bash -e
#
# Hack for adding htcondenser package to system
CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=$PYTHONPATH:$PWD/mc-production/scripts
export PATH=$PATH:$CDIR/mc-production/scripts
