#!/bin/bash

mkdir -p build/code
pip3.6 install -r requirements.txt -t build/code
cp main.py build/code

aws cloudformation package \
   --template-file template.yaml \
   --output-template-file packaged.yaml \
   --s3-bucket $1

aws cloudformation deploy  --capabilities CAPABILITY_IAM --template-file packaged.yaml --stack-name  $2 --region $3