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
    res['created'] = datetime.datetime.strptime(response.get('created'),'%Y-%m-%d %H:%M:%S')
    return FetcherDetails(**res)

def _fetcherlist(response: dict) -> FetcherList:
    """Parse the fetcher list."""
    items = [_fetcherDetails(e) for e in response.get('items',[])]
    pages = response.get('pageCount')
    page = response.get('page')
    return FetcherList(fetched_items=items, pages=pages, page=page)
"""Data schemas for fetcher.

Dribia 2021/04/21, Oleguer Sagarra <ula@dribia.com>  # original author
"""

import datetime
from enum import Enum
from typing import List

from driganttic.schemas.base import Base


class ErrorMessage(str, Enum):
    """Error message options."""

    API_ERROR: str = "API_ERROR"


class FetcherDetails(Base):
    """Fetcher Details schema.

    Warning: Timestamps are time aware!
    """
    id: str
    fetched_timestamp: datetime.datetime = datetime.datetime.now()
    status: str
    name: str
    created: datetime.datetime


class FetcherList(Base):
    """Fetcher List schema."""

    fetched_timestamp: datetime.datetime = datetime.datetime.now()
    fetched_items: List[FetcherDetails]
    pages: int
    page: int


class ResourceList(FetcherList):
    """Resource List schema."""


class TaskList(FetcherList):
    """Task List schema."""


class ProjectList(FetcherList):
    """Project List schema."""


class ResourceDetails(FetcherDetails):
    """Resource List schema."""
    # TODO: Add custom datafields (tipus?)


class TaskDetails(FetcherDetails):
    """Task List schema."""
    projectId: str
    resources: List[str]
    start: datetime.datetime
    end: datetime.datetime
    utilizationPercent: int


class ProjectDetails(FetcherDetails):
    """Project List schema."""
    # TODO: Add custom datafields (esperat, etc)

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
    return _fetcherlist(response)


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
    return _fetcherlist(response)


def _taskdetails(response: dict) -> TaskDetails:
    """Parse the task details response.

    Args:
        response: Ganttic API response

    Returns: Resource Details Pydantic.
    """
    res = response.copy()
    res['start'] = datetime.datetime.strptime(response.get('start'),'%Y-%m-%d')
    res['end'] = datetime.datetime.strptime(response.get('end'),'%Y-%m-%d')
    return TaskDetails(**res)