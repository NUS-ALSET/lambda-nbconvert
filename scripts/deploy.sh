#!/bin/bash

myname="$(basename "$0")"

if [ $# -ne 4 ]
then
    cat<<END
Usage:

    $myname <s3-bucket-name> <stack-name> <aws-region> [<enable-CORS>]

Example:

    $myname lambda-nbconvert lambda-nbconvert-1 us-east-1 Yes

    $myname lambda-nbconvert lambda-nbconvert-2 ap-southeastl-1 No

END
    exit 1
fi

bucket="$1"
stackname="$2"
region="$3"
ENABLE_CORS="${4:-Yes}"

set -e
"$(dirname "$0")"/link.sh

rm -f lambda-nbconvert.zip lambda-nbconvert-overlay.tgz
tar cf - overlay|gzip -c -9 > lambda-nbconvert-overlay.tgz
overlay_s3url="s3://$bucket/$stackname/lambda-nbconvert-overlay.tgz"
aws s3 cp --acl public-read lambda-nbconvert-overlay.tgz "$overlay_s3url"
sed -i "s!^OVERLAY_S3URL *=.*!OVERLAY_S3URL = '$overlay_s3url'!" main.py
zip -ry9 lambda-nbconvert.zip index.html main.py s3cat main.78615eaa.js build

aws cloudformation package \
   --template-file template.yaml \
   --output-template-file packaged.yaml \
   --s3-bucket "$bucket"

aws cloudformation deploy       \
    --capabilities CAPABILITY_IAM   \
    --template-file packaged.yaml   \
    --stack-name "$stackname"       \
    --region "$region"           \
    --parameter-overrides ParameterKey=EnableCORS,ParameterValue=$ENABLE_CORS

