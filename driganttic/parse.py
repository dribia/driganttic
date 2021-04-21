"""Ganttic API response parser.

We parse the anttic API responses as Pydantic models.

Dribia 2021/04/21, Oleguer Sagarra <ula@dribia.com>  # original author
"""

# External modules
import datetime

# Internal modules
from driganttic.schemas.fetcher import (
    ProjectDetails,
    ProjectList,
    ResourceDetails,
    ResourceList,
    TaskDetails,
    TaskList,
    FetcherDetails,
    FetcherList,
)

def _fetcherDetails(response: dict) -> FetcherDetails:
    """Parse the fetcher details"""
    res = response.copy()
    res['created'] = datetime.datetime(response.get('created'),'%Y-%m-%d %H:%M')
    return FetcherDetails(**res)

def _fetcherlist(response: dict) -> FetcherList:
    """Parse the fetcher list."""
    items = [_fetcherDetails(e) for e in response.get('items',[])]
    pages = response.get('pageCount')
    page = response.get('page')
    return FetcherList(items=items, pages=pages, page=page)

def _resourcelist(response: dict) -> ResourceList:
    """Parse the resource response.

    Args:
        response: Ganttic API response

    Returns: Resource List Pydantic.
    """
    raise NotImplementedError("TBD")


def _resourcedetails(response: dict) -> ResourceDetails:
    """Parse the resource details response.

    Args:
        response: Ganttic API response

    Returns: task Details Pydantic.
    """
    raise NotImplementedError("TBD")


def _tasklist(response: dict) -> TaskList:
    """Parse the task response.

    Args:
        response: Ganttic API response

    Returns: task List Pydantic.
    """
    raise NotImplementedError("TBD")


def _projectdetails(response: dict) -> ProjectDetails:
    """Parse the project details response.

    Args:
        response: Ganttic API response

    Returns: project Details Pydantic.
    """
    raise NotImplementedError("TBD")


def _projectlist(response: dict) -> ProjectList:
    """Parse the project response.

    Args:
        response: Ganttic API response

    Returns: project List Pydantic.
    """
    raise NotImplementedError("TBD")


def _taskdetails(response: dict) -> TaskDetails:
    """Parse the task details response.

    Args:
        response: Ganttic API response

    Returns: Resource Details Pydantic.
    """
    raise NotImplementedError("TBD")
