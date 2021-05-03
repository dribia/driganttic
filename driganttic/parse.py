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
from typing import Any, Callable, Dict, List, Optional, Union

import dateparser

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
    created = parse_timestamp(response.get("created"))
    if created is not None:
        res["created"] = created
    if resource_name not in DETAIL_PARSERS.keys():
        return FetcherDetails(**res)
    else:
        return DETAIL_PARSERS[resource_name](res, Translator)


def _refine_taskdetails(response: Dict, Translator: DataFields) -> TaskDetails:
    """Parse the task details response.

    Args:
        response: Ganttic API response
        Translator: Description of task fields

    Returns: Resource Details Pydantic.
    """
    res = response.copy()
    start = parse_timestamp(response.get("start"))
    if start is not None:
        res["start"] = start
    end = parse_timestamp(response.get("end"))
    if end is not None:
        res["end"] = end
    return TaskDetails(**res)


def _refine_resourcedetails(response: Dict, Translator: DataFields) -> ResourceDetails:
    """Parse the resource details response.

    Args:
        response: Ganttic API response
        Translator: Description of  fields

    Returns: task Details Pydantic.
    """
    n_interest_fields = {"Max dedicació facturable": "dedicacio"}
    c_interest_fields = {"Role": "rol"}
    # TODO: This is terrible, but invovles
    #  changing the datafield definition
    # TODO Fix this, parsing is hellish!
    res = response.copy()
    # parse numbers
    nv = response.get("dataFields", {}).get("numbers", [])
    if nv:
        for k, v in n_interest_fields.items():
            val = get_number(nv, k, Translator.numbers)
            if val is not None:
                res[v] = val
    # parse cats
    lv = response.get("dataFields", {}).get("listValues", [])
    if lv:
        for k, v in c_interest_fields.items():
            val = get_category(lv, k, Translator.listValues)
            if val is not None:
                res[v] = val
    return ResourceDetails(**res)


def _refine_projectdetails(response: Dict, Translator: DataFields) -> ProjectDetails:
    """Parse the project details response.

    Args:
        response: Ganttic API response
        Translator: Pydantic Translator model

    Returns: project Details Pydantic.
    """
    n_interest_fields = {
        "Equip": "team",
        "Probabilitat": "probability",
        "Sprints": "sprints",
    }
    c_interest_fields = {"Tipus": "service", "Escenari": "scenario"}
    # TODO: This is terrible, but invovles
    #  changing the datafield definition
    # TODO Fix this, parsing is hellish!
    res = response.copy()
    # parse dates
    dateAproxStart = response["dataFields"].get(
        Translator.dates["Data aproximada d'inici"]
    )
    if dateAproxStart is not None:
        dateAproxStart = parse_timestamp(dateAproxStart)
        if dateAproxStart is not None:
            res["dateAproxStart"] = dateAproxStart
    # parse numbers
    nv = response.get("dataFields", {}).get("numbers", [])
    if nv:
        for k, v in n_interest_fields.items():
            val = get_number(nv, k, Translator.numbers)
            if val is not None:
                res[v] = val
    # parse cats
    lv = response.get("dataFields", {}).get("listValues", [])
    if lv:
        for k, v in c_interest_fields.items():
            val = get_category(lv, k, Translator.listValues)
            if val is not None:
                res[v] = val
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


def _refine_resourcelist(response: Dict, Translator=DataFields) -> ResourceList:
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
    "task": _refine_taskdetails,
    "resource": _refine_resourcedetails,
    "project": _refine_projectdetails,
}
LIST_PARSERS: Dict[str, Callable] = {
    "task": _refine_tasklist,
    "resource": _refine_resourcelist,
    "project": _refine_projectlist,
}

# TODO: Evaluate if a better dependency
#  can be used on none_type (it's only to define NAT)


def parse_timestamp(timeval: Optional[str], none_type=None) -> datetime.datetime:
    """Parses timestamps robustly."""
    if timeval is not None:
        return dateparser.parse(timeval)
    else:
        return none_type


def get_number(
    listitems: List, item_name: str, Translator_field: Dict
) -> Optional[float]:
    """Gets number from translator by name."""
    trans = Translator_field.get(item_name)
    if trans:
        val_comp = [n["number"] for n in listitems if n["id"] == trans]
        if len(val_comp) > 0:
            return val_comp[0]
        else:
            return None
    else:
        raise NameError("No such item name in Translator")


def get_category(listitems: List, item_name: str, Translator_field: Dict) -> Any:
    """Gets category from translator by name."""
    trans = Translator_field.get(item_name, {})
    trans_id = trans.keys()
    if trans:
        val_comp = [
            trans[n["id"]][n["valueId"]] for n in listitems if n["id"] in trans_id
        ]
        if len(val_comp) > 0:
            return val_comp[0]
        else:
            return None
    else:
        raise NameError("No such item name in Translator")
