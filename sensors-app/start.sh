#!/usr/bin/env bash

set -e
set -x

PORT=${PORT:-5000}
WORKERS=${WORKERS:-4}

gunicorn \
    --bind 0.0.0.0:${PORT} \
    --workers ${WORKERS} \
    --worker-class eventlet \
    --access-logfile - \
    "sensorsapp.app:create_app()"
