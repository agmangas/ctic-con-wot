#!/usr/bin/env bash

set -e
set -x

: "${INFLUX_BUCKET:?}"
: "${INFLUX_ORG:?}"
: "${INFLUX_USER:?}"
: "${INFLUX_PASS:?}"
: "${INFLUX_TOKEN:?}"
: ${INFLUX_HOST:="http://influx:8086"}

influx ping --host ${INFLUX_HOST}

influx setup \
    -f \
    -t ${INFLUX_TOKEN} \
    --host ${INFLUX_HOST} \
    -b ${INFLUX_BUCKET} \
    -o ${INFLUX_ORG} \
    -u ${INFLUX_USER} \
    -p ${INFLUX_PASS} || true

# Add a Database / Retention Policy mapping for v1 compatibility

BUCKET_ID=$(influx bucket list --name ${INFLUX_BUCKET} --hide-headers | awk '{print $1}' || "")

if [ -n "$BUCKET_ID" ]; then
    influx v1 dbrp create \
        --db ${INFLUX_BUCKET} \
        --rp rp \
        --bucket-id ${BUCKET_ID} \
        --default || true
fi
