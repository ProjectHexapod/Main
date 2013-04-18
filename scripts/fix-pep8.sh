#!/bin/bash

# Pep8 fixing script for ProjectHexapod 
# by Ian Katz, 2013
# ifreecarve@gmail.com


# usage function to display help for the hapless user

usage ()
{
     mycmd=`basename $0`
     echo "$mycmd"
     echo "usage: $mycmd <File or directory to fix>"
     echo 
     echo "Fixes various pep8 errors in-place.  Can run on a file or recursively on a directory"
}


# test if we have an arguments on the command line
if [ $# -lt 1 ]
then
    usage
    exit 1
fi

# do a pep8 check.  extract the filenames and only show the unique ones. 
#  then use that to build autopep8 commands, and pipe that back to the shell
pep8 $1 | awk -F":" '{print $1}' |uniq |xargs -I{} echo "autopep8 -i --select=E101,E127,E128,E201,E202,E211,E222,E225,E226,E227,E228,E231,E251,E261,E262,E271,E301,E302,E401,E502,E701,E702,E703,W191,W391,W602 {}"  |sh
