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

import os
import dateparser
import yaml

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

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    with open(ROOT_DIR+"/config/config.yaml", "r") as f:
        CUSTOM_FIELDS = yaml.load(f, Loader=yaml.FullLoader).get("custom_fields", {})
except FileNotFoundError:
    CUSTOM_FIELDS = {}


# TODO: Probably can simplify return types
def _fetcherdetails(
    response: Dict,
    resource_name: str,
    Translator: DataFields,
    custom_fields: Dict = CUSTOM_FIELDS,
) -> Union[FetcherDetails, TaskDetails, ResourceDetails, ProjectDetails]:
    """Parse the fetcher details."""
    res = response.copy()
    # parse custom details
    # Here pass your custom fields
    for k_c, v_c in custom_fields.get(resource_name, {}).items():
        lv = response.get("dataFields", {}).get(k_c, [])
        if lv:
            for k, v in v_c.items():
                val2 = GET_FIELDS[k_c](lv, k, Translator.__getattribute__(k_c))
                if val2 is not None:
                    res[v] = val2
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
    res = response.copy()
    # custom parsing
    return ResourceDetails(**res)


def _refine_projectdetails(response: Dict, Translator: DataFields) -> ProjectDetails:
    """Parse the project details response.

    Args:
        response: Ganttic API response
        Translator: Pydantic Translator model

    Returns: project Details Pydantic.
    """
    res = response.copy()
    # custom parsing
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
    """Parse the tasklist response.

    Args:
        response: Ganttic API response
        Translator: Description of  fields

    Returns: task List Pydantic.
    """
    return TaskList(**response)


def _refine_resourcelist(response: Dict, Translator=DataFields) -> ResourceList:
    """Parse the resource list response.

    Args:
        response: Ganttic API response
        Translator: Description of  fields

    Returns: Resource List Pydantic.
    """
    return ResourceList(**response)


def _refine_projectlist(response: Dict, Translator=DataFields) -> ProjectList:
    """Parse the project list response.

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


def parse_timestamp(
    timeval: Optional[str], none_type=None
) -> Optional[datetime.datetime]:
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
        raise NameError(f"No such item name in Translator: {item_name}")


def get_date(
    listitems: List, item_name: str, Translator_field: Dict
) -> Optional[datetime.datetime]:
    """Gets date from translator by name."""
    trans = Translator_field.get(item_name)
    if trans:
        val_comp = [n["date"] for n in listitems if n["id"] == trans]
        if len(val_comp) > 0:
            return parse_timestamp(val_comp[0])
        else:
            return None
    else:
        raise NameError(f"No such item name in Translator: {item_name}")


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
        raise NameError(f"No such item name in Translator: {item_name}")


def get_user() -> Any:
    """Gets user from translator by name."""
    raise NotImplementedError("Not implemented")


def get_text() -> Any:
    """Gets text from translator by name."""
    raise NotImplementedError("Not implemented")


GET_FIELDS: Dict[str, Callable] = {
    "listValues": get_category,
    "numbers": get_number,
    "dates": get_date,
    "texts": get_text,
    "users": get_user,
}
