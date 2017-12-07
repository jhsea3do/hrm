#!/bin/sh
APP_HOME=$(dirname $(realpath $0))/..
PYTHON_HOME=${PYTHON_HOME:-/home/py3}
[ ! -d "$APP_HOME/py" ] && \
    virtualenv -p $PYTHON_HOME/bin/python --prompt "(hrm)" $APP_HOME/py

for req in $(ls $APP_HOME/requirements*.txt); do
    $APP_HOME/py/bin/pip install -q -r $req
done
