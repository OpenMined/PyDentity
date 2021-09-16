#!/usr/bin/env bash

cd "$(dirname "$0")" || exit
CONTAINER_RUNTIME=${CONTAINER_RUNTIME:-docker}

CONTAINER_NAME=process-openapi
${CONTAINER_RUNTIME} build -t ${CONTAINER_NAME} -f ../Dockerfile.process-openapi .
${CONTAINER_RUNTIME} run --name ${CONTAINER_NAME} --rm -it \
    -v "$(pwd)/../data/openapi.yml:/app/openapi.yml:z" \
    -v "$(pwd)/../data/operation-id-map.yml:/app/operation-id-map.yml:z" \
    -v "$(pwd)/../process-openapi.py:/app/process-openapi.py:z" \
    ${CONTAINER_NAME} python /app/process-openapi.py