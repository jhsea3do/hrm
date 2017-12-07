#!/bin/sh
PRJ_HOME=$(dirname $(realpath $0))/..

rm -rf $PRJ_HOME/lib
mkdir -p $PRJ_HOME/lib/hrm

cp -rf $PRJ_HOME/src/* $PRJ_HOME/lib/hrm/
