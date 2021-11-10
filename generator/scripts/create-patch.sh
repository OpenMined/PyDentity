#!/usr/bin/env bash

cd "$(dirname "$0")" || exit

cp ../data/openapi.yml ../data/openapi-updated.yml
sh ./convert-to-openapi3-remote.sh
sh ./process-openapi.sh

cd ..

git diff --no-index --patch data/openapi.yml data/openapi-updated.yml > data/openapi.patch

# Move back to the updated file
mv data/openapi-updated.yml data/openapi.yml

# Replace openapi-updated references with openapi
sed -i '' 's/a\/data\/openapi.yml/a\/generator\/data\/openapi.yml/g' data/openapi.patch
sed -i '' 's/b\/data\/openapi-updated.yml/b\/generator\/data\/openapi.yml/g' data/openapi.patch
