"""Data schemas for fetcher.

Dribia 2021/04/21, Oleguer Sagarra <ula@dribia.com>  # original author
"""

import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from driganttic.schemas.base import Base


class ErrorMessage(str, Enum):
    """Error message options."""

    API_ERROR: str = "API_ERROR"


# Enums


class ServiceEnum(str, Enum):
    """Standard Enum."""

    projecte = "Projecte"
    manteniment = "Manteniment"
    intern = "Intern"
    discovery = "Discovery"
    peed = "PEED"


class RolEnum(str, Enum):
    """Standard Enum."""

    soci = "Soci"
    bd = "BD"
    lds = "LDS"
    ds = "DS"


class ScenarioEnum(str, Enum):
    """Standard Enum."""

    esperat = "Esperat"
    optimista = "Optimista"
    congelat = "Congelat"


class FetcherDetails(Base):
    """Fetcher Details schema.

    Warning: Timestamps are time aware!
    """

    id: str
    fetched_timestamp: datetime.datetime = datetime.datetime.now()
    status: str
    name: str
    created: Optional[datetime.datetime]


class FetcherList(Base):
    """Fetcher List schema."""

    fetched_timestamp: datetime.datetime = datetime.datetime.now()
    fetched_items: List[FetcherDetails]
    pages: int
    page: int


class ResourceDetails(FetcherDetails):
    """Resource List schema."""

    dedicacio: float
    rol: RolEnum

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

    dateAproxStart: datetime.datetime
    team: float
    probability: float
    service: ServiceEnum
    scenario: ScenarioEnum

    # TODO: Add custom datafields (esperat, etc)


class DataFields(Base):
    """Data fields model for API."""

    dates: Dict = {}
    numbers: Dict = {}
    listValues: Any = {}
    texts: Dict = {}
    users: Dict = {}


class ResourceList(FetcherList):
    """Resource List schema."""

    fetched_items: List[ResourceDetails]


class TaskList(FetcherList):
    """Task List schema."""

    fetched_items: List[TaskDetails]


class ProjectList(FetcherList):
    """Project List schema."""

    fetched_items: List[ProjectDetails]
