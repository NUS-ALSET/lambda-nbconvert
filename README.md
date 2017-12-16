# AWS SAM Jupyter 

AWS SAM project that allows invoking Jupyter notebooks dynamically using the AWS Lambda as the execution environment.


### Test your application locally ###

Use [SAM Local](https://github.com/awslabs/aws-sam-local) to run your Lambda function locally:
    
    ./link.sh  # Installs and links all Python dependencies to the current directory
    sam local start-api
    ./unlink.sh # Unlinks all dependencies from the current directory

### Deploy ###

Everything can be deployed with a single command

    ./deploy.sh <Bucket-Name> <Stack-Name> <Region>
