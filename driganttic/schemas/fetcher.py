"""Data schemas for fetcher.

Dribia 2021/04/21, Oleguer Sagarra <ula@dribia.com>  # original author
"""

import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence

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
    confirmat = "Confirmat"


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
    fetched_items: Sequence[FetcherDetails]
    pages: int
    page: int


class ResourceDetails(FetcherDetails):
    """Resource List schema."""

    dedicacio: float
    rol: RolEnum


class TaskDetails(FetcherDetails):
    """Task List schema."""

    # could be holidays
    projectId: Optional[str]
    resources: List[str]
    start: datetime.datetime
    end: datetime.datetime
    utilizationPercent: Optional[float]


class ProjectDetails(FetcherDetails):
    """Project List schema."""

    dateAproxStart: Optional[datetime.datetime]
    team: Optional[float]
    probability: Optional[float]
    service: ServiceEnum
    scenario: ScenarioEnum
    sprints: Optional[float]


# Note: We are adding a method here and this is not totally clean,
# but it's handy, because managing datafields is messy.


class DataFieldsEnum(str, Enum):
    """Standard enum."""

    listValues = "listValues"
    numbers = "numbers"


class DataFields(Base):
    """Data fields model for API."""

    dates: Dict = {}
    numbers: Dict = {}
    listValues: Any = {}
    texts: Dict = {}
    users: Dict = {}


class ResourceList(FetcherList):
    """Resource List schema."""

    fetched_items: Sequence[ResourceDetails]


class TaskList(FetcherList):
    """Task List schema."""

    fetched_items: Sequence[TaskDetails]


class ProjectList(FetcherList):
    """Project List schema."""

    fetched_items: Sequence[ProjectDetails]
