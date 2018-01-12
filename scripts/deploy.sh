#!/bin/bash

rm -rf build
mkdir -p build/code
docker run --user=$UID --entrypoint=/bin/bash -it  -v $PWD:/var/task lambci/lambda:build-python3.6 ./scripts/package.sh
cp main.py build/code

aws cloudformation package \
   --template-file template.yaml \
   --output-template-file packaged.yaml \
   --s3-bucket $1

aws cloudformation deploy  --capabilities CAPABILITY_IAM --template-file packaged.yaml --stack-name  $2 --region $3