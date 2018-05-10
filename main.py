import os
import sys
import ast
import tempfile

CURRENT_DIR = os.getcwd()
BUILD_DIR = os.path.join(os.getcwd(), "build", "code")

sys.path.append(CURRENT_DIR)
sys.path.append(BUILD_DIR)

os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'] + ":" + CURRENT_DIR + ":" + BUILD_DIR




import logging
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from io import StringIO
import json

from timeit import default_timer as timer
logger = logging.getLogger(__name__)


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

# print(homepage)

def handler(event, context):
    
    # !ls
    print(event)
    print("--body-")
    print(event["body"])
    print("--End body--")
    # print(event["body"].keys())
    print(type(event["body"]))
    # files = ast.literal_eval(event["body"])
    if(event["body"]):
        files = json.loads(event["body"])
        print("----------Files--------")
        print(files)
        print(len(files))
    # print(d['notebook'])
        print("-------files inside container--------------")
        # os.chdir('/tmp')
        # tmpdir = tempfile.TemporaryDirectory()
        # os.chdir(tmpdir)
        with open('data1.txt', 'w') as outfile:
            json.dump(files['text'], outfile)
        os.listdir()
        print("----------------end-------------")

    if event['httpMethod'] == 'GET':
        print("------ THIS IS A GET ------")
        response = {
            "statusCode": 200,
            "body": homepage,
            "headers": {
                'Content-Type': 'text/html',
            }
        }
        return response
    else:
        start = timer()
        print("------ NOT A GET ------")
        print("Should process notebook here before returning JSON")
        
        # result = execute_notebook(event["body"])
        result = execute_notebook(json.dumps(files['notebook']))
        # print("------------Result---------")
        # print(type(result))
        result = json.loads(result)
        end = timer()
        duration = end - start
        response = {
            "statusCode": 200,
            "body": json.dumps({"duration": duration,"ipynb": result}),
            "headers": {
                'Content-Type': 'application/json',
            }
        }
        return response