#!/bin/bash

export SERVICE_VERSION=`cat VERSION`
export README_MD=`cat README.md`

#cd src/ska_src_mm_image_discovery_api/rest

env

# set the root path for openapi docs (https://fastapi.tiangolo.com/advanced/behind-a-proxy/)
# this should match any proxy path redirect
cmd="src.ska_src_mm_image_discovery_api.rest.server:app --host "0.0.0.0" --port 8080 --reload --reload-dir src/ska_src_mm_image_discovery_api/ --reload-dir etc/ --reload-include *.json"

# Adding api root path if it is in the environment
if [ ! -z "API_ROOT_PATH" -a "$API_ROOT_PATH" != "" ]; then
  cmd+=' --root-path '$API_ROOT_PATH
fi

echo $cmd

echo $cmd | xargs uvicorn
