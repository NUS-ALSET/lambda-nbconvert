# AWS SAM Jupyter 

AWS SAM project that allows invoking Jupyter notebooks dynamically using the AWS Lambda as the execution environment.




### Test your application locally ###

If running the API for the first time, or **when requirements.txt** file was updated, the following script
should be executed first:

    ./scripts/link.sh
    
It will install and build all dependencies against the Amazon Linux and will place them in the `build/code` 
directory.


Use [SAM Local](https://github.com/awslabs/aws-sam-local) to run your Lambda function locally:

    sam local start-api
    
The API will be running at[http://localhost:3000](http://localhost:3000)

### Deploy ###

Everything can be deployed with a single command

    ./scripts/deploy.sh <Bucket-Name> <Stack-Name> <Region>



### Upload files that can be referenced by the notebook

Selecting one or multiple files will encode those files using Base64 encoding and contents
will be uploaded to the working directory of the Jupyter Notebook.

The total size of all files should not exceed 3 MB in Base64 encoding.

Selecting a single file will also put it's contents to the corresponding text field for further preview.
