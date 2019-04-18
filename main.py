import os
import sys
import ast
import tempfile

CURRENT_DIR = os.getcwd()
BUILD_DIR = os.path.join(os.getcwd(), "build", "code")
OVERLAY_DIR = "/tmp/overlay"
OVERLAY_S3URL = 's3://lambda-nbconvert/lambda-nbconvert-4/lambda-nbconvert-overlay.tgz'

if not os.path.exists(OVERLAY_DIR):
    if 0 == os.system("cd /tmp && /var/task/s3cat '{}'|tar xzf -".format(OVERLAY_S3URL)):
        print('Successfully downloaded and installed the overlay package!')
    else:
        print('Failed to download and/or install the overlay package!')

sys.path.append(CURRENT_DIR)
sys.path.append(BUILD_DIR)
sys.path.append(OVERLAY_DIR)

os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'] + ":" + CURRENT_DIR + ":" + BUILD_DIR + ":" + OVERLAY_DIR




import logging
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from io import StringIO
import json
import base64

from timeit import default_timer as timer
logger = logging.getLogger(__name__)


def return_result_json():
    os.chdir('/tmp')
    if(os.path.isfile('results.json')):
        result_file_reader = open('results.json','r')
        result_file = result_file_reader.read()
        return result_file

def base64_decode_and_persist(filename, contents):
    os.chdir('/tmp')
    decoded = base64.b64decode(contents)
    with open(filename, 'wb') as outfile:
        outfile.write(decoded)
        

def save_files_to_temp_dir(files):
    for key in files:
        print("Processing file: " + key)
        base64_decode_and_persist(key, files[key])


def execute_notebook(source):
    """

    :param source: Jupyter Notebook
    :return: Result of the notebook invocation
    """

    logger.debug("Executing notebook")
    in_memory_source = StringIO(source)
    nb = nbformat.read(in_memory_source, as_version=4)

    logger.debug("Launching kernels")
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3', allow_errors=True)
    ep.preprocess(nb, {'metadata': {'path': '/tmp/'}})

    ex = StringIO()
    nbformat.write(nb, ex)

    logger.debug("Returning results")
    return ex.getvalue()

homepage = ""
with open('index.html') as f:
    homepage=f.read()

def populate_cors(response):
    response['headers']['Access-Control-Allow-Origin'] = os.environ.get('CORS_DOMAIN', '*')
    response['headers']['Access-Control-Allow-Headers'] = os.environ.get('CORS_HEADERS', 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token')
    response['headers']['Access-Control-Allow-Methods'] = os.environ.get('CORS_METHODS', 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT')


def handler(event, context):

    cors_enabled = os.environ.get('ENABLE_CORS', 'false') == 'true'

    if event['httpMethod'] == 'GET':
        response = {
            "statusCode": 200,
            "body": homepage,
            "headers": {
                'Content-Type': 'text/html',
            }
        }
        return response
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
    else:
        request_body = json.loads(event["body"])

        notebook_source = request_body['notebook']
        attached_files = request_body['files'] if 'files' in request_body else {}
        save_files_to_temp_dir(attached_files)



        start = timer()        
        result = execute_notebook(json.dumps(notebook_source))
        result = json.loads(result)

        exec_result = return_result_json()

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

        return response
