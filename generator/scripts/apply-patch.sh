#!/usr/bin/env bash

cd "$(dirname "$0")" || exit

# Apply the patches required
cd .. && git apply --verbose data/openapi.patch