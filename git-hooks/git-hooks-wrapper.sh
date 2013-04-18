#!/bin/bash

# wrapper for any & all git hooks.
# inspired by http://stackoverflow.com/a/3464399/2063546

BASEDIR=$(git rev-parse --show-toplevel)
SCRIPTNAME=$(basename $0)

# look for local hook and run it
if [ -x $BASEDIR/.git/hooks/$SCRIPTNAME.local ]; then
    echo "Running $0.local"
    $0.local "$@" || exit $?
fi

# look for repository-based hook and run it
if [ -x $BASEDIR/git-hooks/$SCRIPTNAME ]; then
    echo "Running $BASEDIR/git-hooks/$SCRIPTNAME"
    $BASEDIR/git-hooks/$SCRIPTNAME "$@" || exit $?
fi
