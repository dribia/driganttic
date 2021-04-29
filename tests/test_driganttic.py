"""driganttic package test module.

Dribia 2021/01/11, Albert Iribarne <iribarne@dribia.com>
"""

import datetime
import os
import pprint
import re

from dotenv import load_dotenv

import driganttic
import driganttic.client as dri_client
import driganttic.parse as dri_parse

# API KEY is stored in the env file
load_dotenv()

APIKEY = os.getenv("APIKEY")


def test_version():
    """Assert that `__version__` exists and is valid."""
    assert re.match(r"\d.\d.\d", driganttic.__version__)


def test_GantticClient():
    """Tester for Ganttic Client class.

    Because all tasks, projects and resources are roughly the same,
    the code is less legible but it iterates the entire
    test with a for loop. Note the test only checks the m
    ethods to work, data validation is made by pyndatinc.
    """
    Client = dri_client.GantticClient(APIKEY=APIKEY)

    # for k in driganttic.client.FETCHERS.keys():
    for k in ["task", "resource", "project"]:
        # test fetcher all
        name2 = f"get_{k}s"
        name4 = f"get_{k}_details"
        if k == "task":
            t1 = datetime.datetime.strptime("2015-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
            t2 = datetime.datetime.strptime("2021-05-01 00:00:00", "%Y-%m-%d %H:%M:%S")
            val1 = Client._get_fetcher(k, timeMin=t1, timeMax=t2)
        else:
            val1 = Client._get_fetcher(k)
        res = val1.json()
        pprint.pprint(f"Sample call {k}:\n {res}")
        # check return
        assert val1.status_code == 200
        val2 = dri_parse._fetcherlist(res, k, Client.Translator[k])
        if k == "task":
            val3 = Client.__getattribute__(name2)(timeMin=t1, timeMax=t2)
        else:
            val3 = Client.__getattribute__(name2)()
        assert val2 == val3
        # test one particualr ID
        resid = res["items"][0].get("id")
        assert resid is not None
        pprint.pprint(val3.dict())
        val11 = Client._get_fetcher(fetcher_name=k, fetcher_detail_id=resid)
        res2 = val11.json()
        pprint.pprint(f"Sample call detailed {k}:\n {res2}")
        assert val1.status_code == 200
        assert res2["id"] == res["items"][0]["id"]
        val2 = dri_parse._fetcherdetails(res2, k, Client.Translator[k])
        val3 = Client.__getattribute__(name4)(resid)
        assert val2 == val3
        pprint.pprint(val3.dict())
        # test data fields
        val21 = Client._get_fetcher(fetcher_name=k, datafields=True)
        res21 = val21.json()
        val22 = dri_parse.__dict__.get("_datafields")(res21)
        val23 = Client.__getattribute__("_get_datafields")(k)
        assert val22 == val23


# test_GantticClient()
