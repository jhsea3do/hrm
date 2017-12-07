#!/bin/sh

APP_HOME=$(dirname $(realpath $0))/..
APP_LIBS=$APP_HOME/lib/hrm
APP_HOST=0.0.0.0
APP_PORT=32897

export FLASK_APP=$APP_LIBS/server/__init__.py

sh $APP_HOME/bin/build.sh
sh $APP_HOME/bin/deploy.sh

$APP_HOME/py/bin/python -m flask run -h $APP_HOST -p $APP_PORT
