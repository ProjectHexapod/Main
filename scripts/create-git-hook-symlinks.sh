#!/bin/bash

# Add hooks for git 
# inspired by http://stackoverflow.com/a/3464399/2063546

HOOK_NAMES="applypatch-msg pre-applypatch post-applypatch pre-commit prepare-commit-msg commit-msg post-commit pre-rebase post-checkout post-merge pre-receive update post-receive post-update pre-auto-gc"

BASEDIR=$(git rev-parse --show-toplevel)

# assuming the script is in a bin directory, one level into the repo
HOOK_DIR="$BASEDIR/.git/hooks"

for hook in $HOOK_NAMES; do
    # If the hook already exists, is executable, and is not a symlink
    if [ ! -h $HOOK_DIR/$hook -a -x $HOOK_DIR/$hook ]; then
        echo "Moving existing hook '$hook' to '$hook.local' (it will still be executed)"
        mv $HOOK_DIR/$hook $HOOK_DIR/$hook.local
    fi
    # create the symlink, overwriting the file if it exists
    # probably the only way this would happen is if you're using an old version of git
    # -- back when the sample hooks were not executable, instead of being named ____.sample
    ln -s -f ../../git-hooks/git-hooks-wrapper.sh $HOOK_DIR/$hook
done
