"""Ganttic API response parser.

We parse the anttic API responses as Pydantic models.

Dribia 2021/04/21, Oleguer Sagarra <ula@dribia.com>  # original author
"""

# External modules
import datetime
from typing import Callable, Dict, List, Union

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


# TODO: Probably can simplify return types
def _fetcherdetails(
    response: Dict, resource_name: str, Translator: DataFields
) -> Union[FetcherDetails, TaskDetails, ResourceDetails, ProjectDetails]:
    """Parse the fetcher details."""
    res = response.copy()
    if response.get("created") is not None:
        res["created"] = datetime.datetime.strptime(
            response.get("created"), "%Y-%m-%d %H:%M:%S"
        )
    else:
        res["created"] = None

    if resource_name not in DETAIL_PARSERS.keys():
        return FetcherDetails(**res)
    else:
        return DETAIL_PARSERS[resource_name](res, Translator)


def _taskdetails(response: Dict, Translator: DataFields) -> TaskDetails:
    """Parse the task details response.

    Args:
        response: Ganttic API response
        Translator: Description of task fields

    Returns: Resource Details Pydantic.
    """
    res = response.copy()
    res["start"] = datetime.datetime.strptime(response.get("start"), "%Y-%m-%d")
    res["end"] = datetime.datetime.strptime(response.get("end"), "%Y-%m-%d")
    return TaskDetails(**res)


def _resourcedetails(response: Dict, Translator: DataFields) -> ResourceDetails:
    """Parse the resource details response.

    Args:
        response: Ganttic API response
        Translator: Description of  fields

    Returns: task Details Pydantic.
    """
    res = response.copy()
    raise NotImplementedError("TBD")
    return ResourceDetails(**res)


def _projectdetails(response: Dict, Translator: DataFields) -> ProjectDetails:
    """Parse the project details response.

    Args:
        response: Ganttic API response
        Translator: Pydantic Translator model

    Returns: project Details Pydantic.
    """
    # TODO: Take out the fields into config
    # This needs careful writting (it's a mess!)
    dateAproxStart = response["dataFields"].get(
        Translator.dates["Data aproximada d'inici"]
    )
    if dateAproxStart is not None:
        dateAproxStart = datetime.datetime.strptime(
            dateAproxStart,
            "%Y-%m-%d %H:%M:%S",
        )
    team = response["dataFields"].get(Translator.numbers["Equip"])
    probability = response["dataFields"].get(Translator.numbers["Probabilitat"])
    # service = response["listValues"][Translator.listValues["Tipus"]]
    # [Translator.listValues['Tipus']]]
    # scenario = Translator.listValues[response['listValues']
    # [Translator.listValues['Tipus']]]
    return ProjectDetails(
        dateAproxStart=dateAproxStart,
        team=team,
        probability=probability,
        # service=service, scenario=scenario
    )


# TODO: Probably can simplify return types
def _fetcherlist(
    response: Dict,
    resource_name: str,
    Translator: DataFields,
) -> Union[FetcherList, TaskList, ResourceList, ProjectList]:
    """Parse the fetcher list."""
    items = [
        _fetcherdetails(e, resource_name, Translator) for e in response.get("items", [])
    ]
    pages = response.get("pageCount")
    page = response.get("page")
    res = {"fetched_items": items, "pages": pages, "page": page}
    if resource_name not in LIST_PARSERS.keys():
        return FetcherList(**res)
    else:
        return LIST_PARSERS[resource_name](res, Translator)


def _tasklist(response: Dict, Translator=DataFields) -> TaskList:
    """Parse the task response.

    Args:
        response: Ganttic API response
        Translator: Description of  fields

    Returns: task List Pydantic.
    """
    return TaskList(**response)


def _resourcelist(response: Dict, Translator=DataFields) -> ResourceList:
    """Parse the resource response.

    Args:
        response: Ganttic API response
        Translator: Description of  fields

    Returns: Resource List Pydantic.
    """
    return ResourceList(**response)


def _projectlist(response: Dict, Translator=DataFields) -> ProjectList:
    """Parse the project response.

    Args:
        response: Ganttic API response
        Translator: Description of  fields

    Returns: project List Pydantic.
    """
    return ProjectList(**response)


def _datafields(response: Dict) -> DataFields:
    """Parse the datafields response.

    It generates a dict that can be referenced by id.
    """
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


DETAIL_PARSERS: Dict[str, Callable] = {
    "task": _taskdetails,
    "resource": _resourcedetails,
    "project": _projectdetails,
}
LIST_PARSERS: Dict[str, Callable] = {
    "task": _tasklist,
    "resource": _resourcelist,
    "project": _projectlist,
}
