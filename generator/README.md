## Generating the client

Currently to generate the client you need to use the DIDx fork of OpenAPI generator and build the JAR yourself.

```sh
# Clone projects
git clone https://github.com/didx-xyz/openapi-generator
git clone https://github.com/didx-xyz/aries-cloudcontroller-python

# Build openapi generator JAR
cd openapi-generator
git checkout feature/new-uplink-generator
mvn -B --no-snapshot-updates clean package -DskipTests=true -Dmaven.javadoc.skip=true -Djacoco.skip=true

# Generate client
cd aries-cloudcontroller-python
pip install -r requirements.tsx
cd generator
./scripts/generate-client.sh
```

## Updating the OpenAPI

Updating the OpenAPI is only needed when a new version of ACA-Py is released. The process of updating the OpenAPI is mostly automated, you only need to run a few scripts. First determine the version you want for OpenAPI spec from the BCGov agent docker images (https://hub.docker.com/r/bcgovimages/aries-cloudagent/). Currently the default for the `retrieve-openapi.sh` script is "py36-1.16-1_0.7.0".

After that you can run the following commands to update the `data/openapi.yml` file. This file should be committed.

```sh
cd aries-cloudcontroller-python/generator

# Retrieve the open api file, change py36-1.16-1_0.7.0 if you want another version
./scripts/retrieve-openapi.sh py36-1.16-1_0.7.0

# transform to OpenAPI V3
./scripts/convert-to-openapi3-local.sh

# If the transform script is not working (e.g. does't work on M1 macs), you can also use an online converter
# This will upload the content to the cloud however
# ./scripts/convert-to-openapi3-remote.sh

# Fix the openapi file (add missing operation ids from data/operation-id-map.yml)
./scripts/process-openapi.sh

# Apply manual patches to the openapi file
./scripts/apply-patch.sh
```

## Updating the patch file

1. Make changes to the OpenAPI file and then run:

```sh
cd aries-cloudcontroller-python/generator

./scripts/create-patch.sh
```
