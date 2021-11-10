#!/usr/bin/env bash

cd "$(dirname "$0")" || exit

curl -X POST https://converter.swagger.io/api/convert -H "Content-Type: application/json" -H "Accept: application/yaml" --data-binary "@../data/swagger.json" -o ../data/openapi.yml