"""Ganttic Client API.

Exceptions:
- TODO: To write

Functions (all are methods within the class):
- TODO: [Post] create something: Task, Resource, Project.
- TODO: [post] edit something: Task, Resource, Project

Dribia 2021/04/21, Oleguer Sagarra <ula@dribia.com>  # original author

The entire Client Class is based on the same logic: It calls one method
that performs the GET queries and then there are wrappers for better
legiblity (like _get_tasks).

To code, check that the returns are well defined pydantinc
schemas (fetcher.py). The parsing is made on the file parse.py.
"""

import datetime
from typing import Dict, Optional, Union

import requests

from driganttic import parse
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

FETCHERS = {
    "resource": {
        "endpoint": "resources",
    },
    "task": {
        "endpoint": "tasks",
    },
    "project": {
        "endpoint": "projects",
    },
}


# TODO: Move defaults to config
# TODO: Async using aiohttp?


class GantticClient:
    """Custom client for the Ganttic API."""

    def __init__(
        self,
        *,
        APIKEY: str,
        ENDPOINT: str = "https://planner.ganttic.com/api",
        VERSION: str = "v1",
        FETCHERS: dict = FETCHERS,
        **kwargs,
    ):
        """Custom Ganttic API Client.

        We implement standard GET methods.

        Args:
            APIKEY: Api key
            ENDPOINT: Api Endpoint
            VERSION: Api version
            FETCHERS: Fetcher list of options
        """
        self.APIKEY = APIKEY
        self.ENDPOINT = ENDPOINT + "/" + VERSION
        self.VERSION = VERSION
        self.FETCHERS = FETCHERS
        self.session = requests.Session()
        # Important: This gets the custom user defined data fields
        self.Translator = dict((k, self._get_datafields(k)) for k in FETCHERS.keys())

    def _get_fetcher(
        self,
        fetcher_name: str,
        fetcher_detail_id: Optional[str] = None,
        datafields=False,
        **kwargs,
    ) -> requests.Response:
        """Main unified method for GET requests.

        Args:
            fetcher_name: One of either task, resource or project
            fetcher_detail_id: Set to a string ID if you want details on
                a resource.
            datafields: Set to True if you want only the custom
                datafields for a fetcher_name

        Returns: Requests response.

        """
        fetcher_endpoint = self.FETCHERS.get(fetcher_name, {}).get("endpoint")
        if fetcher_endpoint is None:
            raise NotImplementedError("Fectcher not implemented")
        if datafields is True:
            if fetcher_detail_id is not None:
                raise ValueError(
                    f"Both datafields {datafields} and id {fetcher_detail_id} cannot be set"
                )
            fetcher_endpoint = fetcher_endpoint + "/" + "datafields"
        if fetcher_detail_id is not None:
            # need to erase the final 's'
            fetcher_endpoint = fetcher_endpoint[:-1] + "/" + str(fetcher_detail_id)
        headers = {"Accept": "application/json"}
        req_string = self.ENDPOINT + "/" + fetcher_endpoint
        kwargs["token"] = self.APIKEY
        with self.session as session:
            # TODO: Implement exception catching
            return session.get(req_string, params=kwargs, headers=headers)

    def _get_datafields(self, fetcher_name: str) -> DataFields:
        """Gets datafields ID-valueID translation for custom fields."""
        return parse._datafields(
            self._get_fetcher(fetcher_name, datafields=True).json()
        )

    def _create_detailed(self, fetcher_name: str, fetcher_details: FetcherDetails):
        """Creates detailed fetcher."""
        # TODO: USe fetchers dict
        raise NotImplementedError("TBD")

    def _modify_detailed(
        self, fetcher_name: str, fetcher_detail_id: str, fetcher_details: FetcherDetails
    ):
        """Creates detailed fetcher."""
        # TODO: USe fetchers dict
        raise NotImplementedError("TBD")

    def _delete_detailed(self, fetcher_name: str, fetcher_detail_id: str):
        """Deletes detailed fetcher."""
        # TODO: USe fetchers dict
        raise NotImplementedError("TBD")

    def _exhaust_pages(self, *args, **kwargs) -> Dict:
        """Exhaust pages from API GET call."""
        rnew = self._get_fetcher(*args, **kwargs).json()
        rfinal = rnew.copy()
        while rnew["page"] < rnew["pageCount"]:
            kwargs["page"] = rnew["page"] + 1
            rnew = self._get_fetcher(*args, **kwargs).json()
            rfinal["items"].extend(rnew["items"])
        return rfinal

    def get_tasks(
        self, timeMin: datetime.datetime, timeMax: datetime.datetime, **kwargs
    ) -> Union[FetcherList, TaskList, ResourceList, ProjectList]:
        """Gets tasks."""
        return parse._fetcherlist(
            self._exhaust_pages(
                "task",
                timeMin=timeMin.strftime("%Y-%m-%d %H:%M"),
                timeMax=timeMax.strftime("%Y-%m-%d %H:%M"),
                **kwargs,
            ),
            "task",
            self.Translator.get("task", DataFields()),
        )

    def get_projects(
        self, **kwargs
    ) -> Union[FetcherList, TaskList, ResourceList, ProjectList]:
        """Gets projects."""
        return parse._fetcherlist(
            self._exhaust_pages("project", **kwargs),
            "project",
            self.Translator.get("project", DataFields()),
        )

    def get_resources(
        self, **kwargs
    ) -> Union[FetcherList, TaskList, ResourceList, ProjectList]:
        """Gets resources."""
        return parse._fetcherlist(
            self._exhaust_pages("resource", **kwargs),
            "resource",
            self.Translator.get("resource", DataFields()),
        )

    def get_task_details(
        self, taskId: str, **kwargs
    ) -> Union[FetcherDetails, TaskDetails, ResourceDetails, ProjectDetails]:
        """Gets details from task."""
        return parse._fetcherdetails(
            self._get_fetcher("task", fetcher_detail_id=taskId, **kwargs).json(),
            "task",
            self.Translator.get("task", DataFields()),
        )

    def get_resource_details(
        self, resourceId: str, **kwargs
    ) -> Union[FetcherDetails, TaskDetails, ResourceDetails, ProjectDetails]:
        """Gets details from resource."""
        return parse._fetcherdetails(
            self._get_fetcher(
                "resource", fetcher_detail_id=resourceId, **kwargs
            ).json(),
            "resource",
            self.Translator.get("resource", DataFields()),
        )

    def get_project_details(
        self, projectId: str, **kwargs
    ) -> Union[FetcherDetails, TaskDetails, ResourceDetails, ProjectDetails]:
        """Gets details from project."""
        return parse._fetcherdetails(
            self._get_fetcher("project", fetcher_detail_id=projectId, **kwargs).json(),
            "project",
            self.Translator.get("project", DataFields()),
        )

    def create_task(self, TaskData: TaskDetails):
        """Creates detailed task."""
        return self._create_detailed("task", TaskData)

    def modify_task(self, taskId: str, TaskData: TaskDetails):
        """Gets stuff."""
        return self._modify_detailed("task", taskId, TaskData)

    def delete_task(self, taskId: str):
        """Gets stuff."""
        return self._delete_detailed("task", taskId)

    def create_resource(self, ResourceData: ResourceDetails):
        """Gets stuff."""
        return self._create_detailed("resource", ResourceData)

    def modify_resource(self, resourceId: str, ResourceData: ResourceDetails):
        """Gets stuff."""
        return self._modify_detailed("resource", resourceId, ResourceData)

    def delete_resource(self, resourceId: str):
        """Gets stuff."""
        return self._delete_detailed("resource", resourceId)

    def create_project(self, ProjectData: ProjectDetails):
        """Gets stuff."""
        return self._create_detailed("project", ProjectData)

    def modify_project(self, projectId: str, ProjectData: ProjectDetails):
        """Gets stuff."""
        return self._modify_detailed("project", projectId, ProjectData)

    def delete_project(self, projectId: str):
        """Gets stuff."""
        return self._delete_detailed("project", projectId)
