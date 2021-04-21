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
    """Tester for Ganttic Client class."""
    Client = dri_client.GantticClient(APIKEY=APIKEY)

    #for k in driganttic.client.FETCHERS.keys():
    for k in ['task']:
        name1 = f'{k}list'
        name2 = f'get_{k}s'
        name3 = f'{k}details'
        name4 = f'get_{k}_details'
        if k == 'task':
            t1 = datetime.datetime.strptime('2021-01-01 00:00:00','%Y-%m-%d %H:%M:%S')
            t2 = datetime.datetime.strptime('2021-05-01 00:00:00','%Y-%m-%d %H:%M:%S')
            val1 = Client._get_fetcher(k, timeMin = t1, timeMax= t2)
        else:
            val1 = Client._get_fetcher(k)
        res = val1.json()
        print(f'Sample call {k}:\n {res}')
        assert(val1.status_code == 200)
        val2 = dri_parse.__dict__.get('_'+name1)(res)
        if k == 'task':
            val3 = Client.__getattribute__(name2)(timeMin = t1, timeMax = t2)
        else:
            val3 = Client.__getattribute__(name2)(k)
        assert(val2==val3)
        resid = res['items'][0].get('id')
        assert(resid is not None)
        val11 = Client._get_fetcher(fetcher_name=k, fetcher_detail_id=resid)
        res2 = val11.json()
        print(f'Sample call detailed {k}:\n {res2}')
        assert(val1.status_code == 200)
        assert(res2['id'] == res['items'][0]['id'])
        val2 = dri_parse.__dict__.get('_'+name3)(res2)
        val3 = Client.__getattribute__(name4)(resid)
        assert(val2==val3)