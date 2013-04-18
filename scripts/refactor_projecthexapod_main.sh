#!/bin/bash

# ProjectHexapod repo refactoring script
# by Ian Katz, 2013
# ifreecarve@gmail.com


# usage function to display help for the hapless user

usage ()
{
     mycmd=`basename $0`
     echo "$mycmd"
     echo "usage: $mycmd <ProjectHexapod/Main repository directory>"
     echo 
     echo "This script MUST be run from the directory _containing_ the ProjectHexapod/Main repository"
}


# test if we have an arguments on the command line
if [ $# -lt 1 ]
then
    usage
    exit 1
fi


echo "Cleaning up from any previous runs..."
for OLD_DIR in $(ls -d projecthexapod-*)
do
    echo " - $OLD_DIR"
    rm -rf $OLD_DIR
done


echo
echo "Creating new sub-repos from subdirectories"
for SUBDIR in "Assignments" "Examples" "Firmware" "Gimpy" "Plotter" "Protoleg" "Stompy" "UI" "Utilities" "electronics"
do
    echo " = $SUBDIR creation ="
    NEWDIR="projecthexapod-$SUBDIR"

    git clone --no-hardlinks $1 $NEWDIR
    pushd $NEWDIR 1>/dev/null
    git remote rm origin

    echo " = $SUBDIR filter-branch = "
    git filter-branch --tag-name-filter cat --prune-empty --subdirectory-filter $SUBDIR -- --all   
 
    echo " = $SUBDIR update reflogs = "
    git reset --hard
    git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d
    git reflog expire --expire=now --all

    echo " = $SUBDIR repack = "
    git repack -ad

    echo " = $SUBDIR gc = "
    git gc --aggressive --prune=now

    echo " = $SUBDIR copy common files = "
    for COMMON in ".gitignore" "LICENSE.txt"
    do
        cp -r "../projecthexapod/$COMMON" ./
    done   

    popd 1>/dev/null
    echo

done

mv projecthexapod-electronics projecthexapod-Electronics


STARKIT="BotKits"
echo
echo "Creating $STARKIT sub-repo by pruning"
NEWDIR="projecthexapod-$STARKIT"
git clone --no-hardlinks projecthexapod $NEWDIR
pushd $NEWDIR 1>/dev/null
git remote rm origin

PRUNE=$(ls |grep -v txt |grep -v Kit | tr "\n" " ")
echo " = $STARKIT Pruning away $PRUNE = "
git filter-branch --tree-filter "rm -rf $PRUNE " --prune-empty HEAD

echo " = $STARKIT update reflogs = "
git reset --hard
git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d
git reflog expire --expire=now --all
    
echo " = $STARKIT repack = "
git repack -ad

echo " = *Kit gc = "
git gc --aggressive --prune=now

popd 1>/dev/null
echo
