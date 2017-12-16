"""
This file contains utility methods needed to execute notebooks
"""
import logging
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from io import StringIO

logger = logging.getLogger(__name__)


