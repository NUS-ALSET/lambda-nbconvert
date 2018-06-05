# AWS SAM Jupyter 

AWS SAM project that allows invoking Jupyter notebooks dynamically using the AWS Lambda as the execution environment.




## Test your application locally ###

If running the API for the first time, or **when requirements.txt** file was updated, the following script
should be executed first:

    ./scripts/link.sh
    
It will install and build all dependencies against the Amazon Linux and will place them in the `build/code` 
directory.


Use [SAM Local](https://github.com/awslabs/aws-sam-local) to run your Lambda function locally:

    sam local start-api
    
The API will be running at[http://localhost:3000](http://localhost:3000)

## Deploy ##

### Preparation
To deploy this SAM project, an existing bucket is required in the target region. It can be created using AWS Management Console.

To create an S3 bucket, use the instructions below:

1. Sign-in to the [AWS Management Console](https://console.aws.amazon.com)

2. Ensure a proper region is selected:
![Select a region](./docs/region-selection.png)

3. Open the S3 Console by finding the corresponding icon in the "Storage" section or by typing "S3" in the service search field:

![S3 Console](./docs/s3-selection.png)

4. Create a new bucket using the "Create bucket" button:
![Create Bucket](./docs/create-bucket.png)


### Deployment
Once the bucket is created, it can be used for the SAM deployment.
Use the "deploy.sh" script and provide all the required parameters:


    ./scripts/deploy.sh <Bucket-Name> <Stack-Name> <Region> <EnableCORS>


**Bucket Name** parameter should have the same value as the name of the bucket that was created in the previous step.

**Stack Name** can be any alphanumeric value without spaces. Using 
some name for the first time creates a new CloudFormation stack, while
all consequent execution of the scrip with the same name will update
the corresponding CF stack rather than create a new one.

**Region** must match the region of the bucket, created earlier.

**EnableCORS** is an optional parameter that can have **Yes** or **No** value depending on whether the CORS should be allowed
for this endpoint.



## Upload files that can be referenced by the notebook

Selecting one or multiple files will encode those files using Base64 encoding and contents
will be uploaded to the working directory of the Jupyter Notebook.

The total size of all files should not exceed 3 MB in Base64 encoding.

Selecting a single file will also put it's contents to the corresponding text field for further preview.

## Implementation details

### CORS Support
To enable cross-origin requests (requests from domains, different from the API domain), a CORS support was implemented.
CORS is enabled by default and can be configured using various parameters of the stack:

```
Parameters:
  EnableCORS:
    Type: String
    Default: Yes
    AllowedValues:
      - Yes
      - No
  CORSDomain:
    Type: String
    Default: "*"
  CORSMethods:
    Type: String
    Default: "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT" 
  CORSHeaders:
    Type: String
    Default: "Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token"  
```

Default values should work in most of the cases. EnableCORS parameter can be supplied via the command line, as it explained in the "Deployment" section of the readme.

Dynamic CORS configuration is achieved by populating response headers programmatically (see the **main.py** file).

Enabled/disabled state is being read from Lambda environment variables, with a default value of 'true' (note it's a string and not a boolean, since the value is passed as an environment variable):

```
    cors_enabled = os.environ.get('ENABLE_CORS', 'false') == 'true'
```

In a case if CORS is enabled, a CORS preflight request/response is implemented:

```
...
elif event['httpMethod'] == 'OPTIONS' and cors_enabled:
        response = {
            "statusCode": 200,
            "body": None,
            "headers": {
                'Content-Type': 'application/json',
            }
        }
        populate_cors(response)     
        return response  
...       
```

And finally, the POST response is being populated with proper CORS headers if CORS is enabled:

```
...
end = timer()
        duration = end - start
        response = {
            "statusCode": 200,
            "body": json.dumps({"duration": duration,"ipynb": result, "result": exec_result}),
            "headers": {
                'Content-Type': 'application/json',
            }
        }

        if cors_enabled:
            populate_cors(response)
...
```