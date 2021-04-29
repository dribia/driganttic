"""Ganttic API response parser.

We parse the anttic API responses as Pydantic models.

Note that the models are custom to Dribia needs, if you need
to change the custom data fields, you need to change each function.

The logic is a follows: There are two base methods (_fetcher) and
(_fetcherDetails) to parse the generic things, and then functions
to refine (taks, project, resource) the speciffic stuff defined
in the pydantic models.

Dribia 2021/04/21, Oleguer Sagarra <ula@dribia.com>  # original author
"""

# External modules
import datetime
from typing import Callable, Dict, List, Optional, Union

import dateparser
import numpy as np

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
    res["created"] = parse_timestamp(response.get("created"))

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
    res["start"] = parse_timestamp(response.get("start"))
    res["end"] = parse_timestamp(response.get("end"))
    return TaskDetails(**res)


def _refine_resourcedetails(response: Dict, Translator: DataFields) -> ResourceDetails:
    """Parse the resource details response.

    Args:
        response: Ganttic API response
        Translator: Description of  fields

    Returns: task Details Pydantic.
    """
    # TODO: This is terrible, but invovles
    #  changing the datafield definition
    # TODO Fix this, parsing is hellish!
    res = response.copy()
    # parse numbers
    nv = response.get("dataFields", {}).get("numbers", [])
    trans_dedicacio = Translator.numbers[
        "Max dedicació facturable"
    ]  # 1st is always the key
    ded = [n["number"] for n in nv if n["id"] == trans_dedicacio][0]
    res["dedicacio"] = float(ded)
    # parse role
    lv = response.get("dataFields", {}).get("listValues", [])
    trans_role = Translator.listValues["Role"]  # 1st is always the key
    role_id = trans_role.keys()
    role = [trans_role[n["id"]][n["valueId"]] for n in lv if n["id"] in role_id][0]
    res["rol"] = role
    return ResourceDetails(**res)


def _refine_projectdetails(response: Dict, Translator: DataFields) -> ProjectDetails:
    """Parse the project details response.

    Args:
        response: Ganttic API response
        Translator: Pydantic Translator model

    Returns: project Details Pydantic.
    """
    res = response.copy()
    dateAproxStart = response["dataFields"].get(
        Translator.dates["Data aproximada d'inici"]
    )
    if dateAproxStart is not None:
        dateAproxStart = parse_timestamp(dateAproxStart)
    res["dateAproxStart"] = dateAproxStart
    # TODO Make a proper class for this mess
    # parse numbers
    nv = response.get("dataFields", {}).get("numbers", [])
    trans_team = Translator.numbers["Equip"]
    trans_prob = Translator.numbers["Probabilitat"]
    # 1st is always the key
    prob = [n["number"] for n in nv if n["id"] == trans_prob][0]
    res["probability"] = float(prob)
    team = [n["number"] for n in nv if n["id"] == trans_team][0]
    res["team"] = float(team)

    # parse listvalues
    lv = response.get("dataFields", {}).get("listValues", [])
    trans_service = Translator.listValues["Tipus"]  # 1st is always the key
    trans_scenario = Translator.listValues["Escenari"]  # 1st is always the key
    service_id = trans_service.keys()
    scenario_id = trans_scenario.keys()
    service = [
        trans_service[n["id"]][n["valueId"]] for n in lv if n["id"] in service_id
    ][0]
    scenario = [
        trans_scenario[n["id"]][n["valueId"]] for n in lv if n["id"] in scenario_id
    ][0]
    res["service"] = service
    res["scenario"] = scenario
    return ProjectDetails(**res)


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


def _refine_tasklist(response: Dict, Translator=DataFields) -> TaskList:
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


def _refine_projectlist(response: Dict, Translator=DataFields) -> ProjectList:
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
    # TODO This probably needs heavy refactor
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
    "resource": _refine_resourcedetails,
    "project": _refine_projectdetails,
}
LIST_PARSERS: Dict[str, Callable] = {
    "task": _refine_tasklist,
    "resource": _resourcelist,
    "project": _refine_projectlist,
}

# TODO: Evaluate if a better dependency
#  can be used on none_type (it's only to define NAT)


def parse_timestamp(
    timeval: Optional[str], none_type=np.datetime64("NaT")
) -> datetime.datetime:
    """Parses timestamps robustly."""
    if timeval is not None:
        return dateparser.parse(timeval)
    else:
        return none_type
