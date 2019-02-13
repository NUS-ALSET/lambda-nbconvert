#!/bin/bash

rm -rf build overlay
mkdir -p build/code
mkdir overlay
docker run --user=$UID --entrypoint=/bin/bash -it --rm -v $PWD:/var/task lambci/lambda:build-python3.6 ./scripts/package.sh
mv build/code/tensorflow overlay
#ln -sv main.py build/code/
