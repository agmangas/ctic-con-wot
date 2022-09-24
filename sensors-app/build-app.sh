#!/usr/bin/env bash

set -e
set -x

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
APP_GIT_PATH="${CURR_DIR}/.."
APP_SPA_PATH="${CURR_DIR}/api/sensorsapp/appjs"

if test -d "${APP_GIT_PATH}/.git"; then
    git clean -x -d -f ${APP_SPA_PATH}
else
    rm -fr ${APP_SPA_PATH}/*
fi

cd ${CURR_DIR}/app
npm install
npm run build
mv ${CURR_DIR}/app/build/* ${APP_SPA_PATH}
