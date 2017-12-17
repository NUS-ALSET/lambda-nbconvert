#!/bin/bash

pwd
scripts/unlink.sh
rm -rf build
mkdir -p build/code
docker run --user=$UID --entrypoint=/bin/bash -it  -v $PWD:/var/task lambci/lambda:build-python3.6 ./scripts/package.sh
ln -sv build/code/* .