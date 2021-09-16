#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/../" || exit

# Remove old generated code
rm -rf ../generated/

# Generated client
java  -ea -server -Duser.timezone=UTC -jar "$(pwd)/../../openapi-generator/modules/openapi-generator-cli/target/openapi-generator-cli.jar" generate -c  ./openapi-generator-config.yml --skip-validate-spec

# Copy 
cp -r ../generated/aries_cloudcontroller/ ../aries_cloudcontroller/

black ..