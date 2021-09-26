#!/bin/bash

for arg; do
  case $1 in
  -l | --local)
    shift && LOCAL=1
    ;;
  -r | --reload)
    shift && RELOAD=1
    ;;
  esac
done

APP='main'
HOST='0.0.0.0'
PORT=3000
WORKERS=4

if [ ! -z ${GUNICORN_WORKERS} ]; then WORKERS=${GUNICORN_WORKERS}; fi

if [ "$LOCAL" = "1" ]; then
  echo "--local option enabled"
  BINPATH=$(dirname $0)
  cd $BINPATH/../../src

  if [ "$RELOAD" = "1" ]; then
    echo "--reload option enabled"
    python -B ${APP}.py
  else
    gunicorn -k uvicorn.workers.UvicornWorker --log-level 'warning' -w ${WORKERS} -b ${HOST}:${PORT} ${APP}
  fi
else
  echo "Starting Application"
  if [ "$RELOAD" = "1" ]; then
    echo "--reload option enabled"
    gunicorn -k uvicorn.workers.UvicornWorker --log-level 'warning' -w ${WORKERS} -b ${HOST}:${PORT} ${APP} --reload
  else
    gunicorn -k uvicorn.workers.UvicornWorker --log-level 'warning' -w ${WORKERS} -b ${HOST}:${PORT} ${APP}
  fi
fi
