import logging
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from io import StringIO

logger = logging.getLogger(__name__)
os.environ['PYTHONPATH'] = os.getcwd()


def execute_notebook(source: str) -> str:
    """

    :param source: Jupyter Notebook
    :return: Result of the notebook invocation
    """

    in_memory_source = StringIO(source)
    nb = nbformat.read(in_memory_source, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': '/tmp/'}})

    ex = StringIO()
    nbformat.write(nb, ex)

    return ex.getvalue()

test_page = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>JS Bin</title>
</head>
<body>
<script>
  
var myAlert = function(){
  console.log("POSTing ipynb text as JSON");
  var x = document.getElementById("myTextarea").value;
  var obj = JSON.parse(x);
  //console.log(obj);
  postData(obj)
}
var postData = function(data){
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function() {
    if (xhr.status === 200) {
        var userInfo = JSON.parse(xhr.responseText);
        console.log(userInfo);
        document.getElementById("responseJSON").value = JSON.stringify(userInfo);
    }
    else{
      console.log("Nope");
      document.getElementById("responseJSON").value = "Nope";
    }
};
xhr.send(JSON.stringify(data)); 
  
}

</script>
<h3>ipynb json to post</h3>
<textarea id="myTextarea" cols=80 rows=20>
{
    "Paste":"ipynb text here"
}  
</textarea><br/>
<button onclick="myAlert()">Post JSON</button> 
<h3>resulting ipynb json returned from lambda</h3>
<textarea id="responseJSON" cols=80 rows=8>
</textarea>

</body>
</html>
"""

default_notebook = """
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "for x in range(10):\n",
    "    print(x)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.5.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
"""

def handler(event, context):
    print(event)
    print("--body-")
    print(event["body"])
    print("--End body--")
    if event['httpMethod'] == 'GET':
        print("------ THIS IS A GET ------")
        response = {
            "statusCode": 200,
            "body": test_page,
            "headers": {
                'Content-Type': 'text/html',
            }
        }
        return response
    else:
        print("------ NOT A GET ------")
        print("Should process notebook here before returning JSON")
        response = {
            "statusCode": 200,
            "body": event["body"],
            "headers": {
                'Content-Type': 'application/json',
            }

        }
        return response