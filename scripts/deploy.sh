#!/bin/bash

set -e
"$(dirname "$0")"/link.sh

rm -f lambda-nbconvert.zip
zip -ry9 lambda-nbconvert.zip index.html main.py main.78615eaa.js build
aws cloudformation package \
   --template-file template.yaml \
   --output-template-file packaged.yaml \
   --s3-bucket "$1"

ENABLE_CORS=${4:-Yes}
aws cloudformation deploy 		\
	--capabilities CAPABILITY_IAM	\
	--template-file packaged.yaml	\
	--stack-name "$2"		\
	--region "$3"		 	\
	--parameter-overrides ParameterKey=EnableCORS,ParameterValue=$ENABLE_CORS

