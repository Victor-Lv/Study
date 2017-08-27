#!/bin/bash

#Jenkins script to trigger lib dependency checker.

#Date    : 2017-05-23
#Author  : Victor Lyu


#The absolute path of the directory assigned to the build as a workspace.
echo -e "\n Workspace path is:\n$WORKSPACE.\nPython version is:"
python2.7 -V

ROOT="$WORKSPACE"

LIB_DEPENDENCY_CHECKER_PATH="$ROOT/BCTools/LibDependencyChecker"

if [ ! -d $LIB_DEPENDENCY_CHECKER_PATH ]; then
	echo -e "\nLIB_DEPENDENCY_CHECKER_PATH do not exist.\n"
	exit 1
fi

python2.7 $LIB_DEPENDENCY_CHECKER_PATH/lib_dependency_check.py -r "$ROOT"
if [ $? -ne 0 ];then 
	echo -e "\nThere are some errors.\n"
	exit 1
fi

exit 0

