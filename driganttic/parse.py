"""Ganttic API response parser.

We parse the anttic API responses as Pydantic models.

Dribia 2021/04/21, Oleguer Sagarra <ula@dribia.com>  # original author
"""

# External modules
import datetime
from typing import Dict, List

# Internal modules
from driganttic.schemas.fetcher import (
    DataFields,
    FetcherDetails,
    FetcherList,
    ProjectDetails,
    ProjectList,
    ResourceDetails,
    ResourceList,
    TaskDetails,
    TaskList,
)


def _fetcherDetails(response: Dict) -> FetcherDetails:
    """Parse the fetcher details."""
    res = response.copy()
    res["created"] = datetime.datetime.strptime(
        response.get("created"), "%Y-%m-%d %H:%M:%S"
    )
    return FetcherDetails(**res)


def _fetcherlist(response: Dict) -> FetcherList:
    """Parse the fetcher list."""
    items = [_fetcherDetails(e) for e in response.get("items", [])]
    pages = response.get("pageCount")
    page = response.get("page")
    return FetcherList(fetched_items=items, pages=pages, page=page)


def _resourcelist(response: Dict) -> ResourceList:
    """Parse the resource response.

    Args:
        response: Ganttic API response

    Returns: Resource List Pydantic.
    """
    return ResourceList(**_fetcherlist(response).dict())


def _resourcedetails(response: Dict) -> ResourceDetails:
    """Parse the resource details response.

    Args:
        response: Ganttic API response

    Returns: task Details Pydantic.
    """
    raise NotImplementedError("TBD")


def _tasklist(response: Dict) -> TaskList:
    """Parse the task response.

    Args:
        response: Ganttic API response

    Returns: task List Pydantic.
    """
    return TaskList(**_fetcherlist(response).dict())


def _projectdetails(response: Dict, Translator: DataFields) -> ProjectDetails:
    """Parse the project details response.

    Args:
        response: Ganttic API response
        Translator: Pydantic Translator model

    Returns: project Details Pydantic.
    """
    # TODO: Take out the fields into config
    dateAproxStart = datetime.datetime.strptime(
        response["dataFields"][Translator.dates["Data aproximada d'inici"]],
        "%Y-%m-%d %H:%M:%S",
    )
    team = response["dataFields"][Translator.numbers["Equip"]]
    probability = response["dataFields"][Translator.numbers["Probabilitat"]]
    # service = Translator.listValues[response['listValues']
    # [Translator.listValues['Tipus']]]
    # scenario = Translator.listValues[response['listValues']
    # [Translator.listValues['Tipus']]]
    return ProjectDetails(
        dateAproxStart=dateAproxStart, team=team, probability=probability
    )


def _projectlist(response: Dict) -> ProjectList:
    """Parse the project response.

    Args:
        response: Ganttic API response

    Returns: project List Pydantic.
    """
    return ProjectList(**_fetcherlist(response).dict())


def _taskdetails(response: Dict) -> TaskDetails:
    """Parse the task details response.

    Args:
        response: Ganttic API response

    Returns: Resource Details Pydantic.
    """
    res = response.copy()
    res["start"] = datetime.datetime.strptime(response.get("start"), "%Y-%m-%d")
    res["end"] = datetime.datetime.strptime(response.get("end"), "%Y-%m-%d")
    return TaskDetails(**res)


def _datafields(response: Dict) -> DataFields:
    """Parse the datafields response."""
    res = response.copy()
    for k, v in res.items():
        if k == "listValues":
            res[k] = dict(
                (
                    vv["name"],
                    {
                        vv["id"]: _exhaust_dict(
                            vv["values"], field_v="value", field_k="id"
                        )
                    },
                )
                for vv in v
            )
        else:
            res[k] = _exhaust_dict(v)
    return DataFields(**res)


def _exhaust_dict(vallist: List, field_v="id", field_k="name") -> Dict:
    """Dict exhauster."""
    return dict((vvv[field_k], vvv[field_v]) for vvv in vallist)
