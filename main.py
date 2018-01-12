import os
import sys


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
    print(event)
    print("--body-")
    print(event["body"])
    print("--End body--")
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
        result = execute_notebook(event["body"])
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