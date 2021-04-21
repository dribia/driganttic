"""driganttic package test module.

Dribia 2021/01/11, Albert Iribarne <iribarne@dribia.com>
"""

import re

import driganttic
import os
from dotenv import load_dotenv

# API KEY is stored in the env file
load_dotenv()

APIKEY = os.getenv('APIKEY')


def test_version():
    """Assert that `__version__` exists and is valid."""
    assert re.match(r"\d.\d.\d", driganttic.__version__)
