"""driganttic package test module.

Dribia 2021/01/11, Albert Iribarne <iribarne@dribia.com>
"""

import re
import datetime

import driganttic
import os
from dotenv import load_dotenv

import driganttic.client as dri_client
import driganttic.parse as dri_parse

# API KEY is stored in the env file
load_dotenv()

APIKEY = os.getenv('APIKEY')

Client = dri_client.GantticClient(APIKEY=APIKEY)

def test_version():
    """Assert that `__version__` exists and is valid."""
    assert re.match(r"\d.\d.\d", driganttic.__version__)

def test_GantticClient():
    Client = dri_client.GantticClient(APIKEY=APIKEY)

    for k in driganttic.client.FETCHERS.keys():
        name1 = f'{k}list'
        name2 = f'get_{k}s'
        if k == 'task':
            t1 = datetime.datetime.strptime('2021-01-01 00:00','%Y-%m-%d %H:%M')
            t2 = datetime.datetime.strptime('2021-05-01 00:00','%Y-%m-%d %H:%M')
            val1 = Client._get_fetcher(k, timeMin = t1, timeMax= t2)
        else:
            val1 = Client._get_fetcher(k)
        assert(resid is not None)
        print(f'Sample call {k}:\n {res}')
        assert(val1.status_code == 200)
        val2 = dri_parse.__getattribute__(name1, val1)
        val3 = Client.__getattribute__(name2, k)
        assert(val2==val3)
        # TODO: Add asserts

        # TODO: Test get detailed
        res = val1.json()
        resid = val1['items'][0].get('id')
