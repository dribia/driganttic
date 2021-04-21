"""Ganttic Client API.

Exceptions:
- TODO: To write

Functions (all are methods within the class):
- [Get] list: Task, Resource, Project
- [Get] details of list element: Task, Resource, Project
- [Post] create something: Task, Resource, Project
- [post] edit something: Task, Resource, Project

Dribia 2021/04/21, Oleguer Sagarra <ula@dribia.com>  # original author

For an explanation on the async,
see here: https://towardsdatascience.com/fast-and-async-in-python-
accelerate-your-requests-using-asyncio-62dafca83c33
"""

# import asyncio
# import json
# import os
from typing import Dict

import parse

# Internal modules
from driganttic.schemas.fetcher import (
    FetcherDetails,
    ProjectDetails,
    ProjectList,
    ResourceDetails,
    ResourceList,
    TaskDetails,
    TaskList,
)

# import aiohttp
# External modules
# import requests
# from aiohttp import ClientSession as ai_ClientSession


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
# TODO: Elegant way to not need to write all funcs (decorator)?


class GantticClient:
    """Custom client for the Ganttic API."""

    def __init__(
        self,
        *,
        APIKEY: str,
        ENDPOINT: str = "https://planner.ganttic.com/api/",
        VERSION: str = "v1",
        FETCHERS: dict = FETCHERS,
        **kwargs,
    ):
        """Custom Ganttic API Client.

        We implement standard methods.

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

    def _get_all(self, fetcher_name: str) -> Dict:
        """Gets list of the entire fetcher."""
        # TODO: USe fetchers dict
        raise NotImplementedError("TBD")

    def _get_detailed(self, fetcher_name: str, fetcher_detail_id: str) -> Dict:
        """Gets details of the detailed fetcher."""
        # TODO: USe fetchers dict
        raise NotImplementedError("TBD")

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

    def get_tasks(self) -> TaskList:
        """Gets stuff."""
        return parse._tasklist(self._get_all("task"))

    def get_task_details(self, taskId: str) -> FetcherDetails:
        """Gets stuff."""
        return parse._taskdetails(self._get_detailed("task", taskId))

    def create_task(self, TaskData: TaskDetails):
        """Creates stuff."""
        return self._create_detailed("task", TaskData)

    def modify_task(self, taskId: str, TaskData: TaskDetails):
        """Gets stuff."""
        return self._modify_detailed("task", taskId, TaskData)

    def delete_task(self, taskId: str):
        """Gets stuff."""
        return self._delete_detailed("task", taskId)

    def get_resources(self) -> ResourceList:
        """Gets stuff."""
        return parse._resourcelist(self._get_all("resource"))

    def get_resource_details(self, resourceId: str) -> ResourceDetails:
        """Gets stuff."""
        return parse._resourcedetails(self._get_detailed("resource", resourceId))

    def create_resource(self, ResourceData: ResourceDetails):
        """Gets stuff."""
        return self._create_detailed("resource", ResourceData)

    def modify_resource(self, resourceId: str, ResourceData: ResourceDetails):
        """Gets stuff."""
        return self._modify_detailed("resource", resourceId, ResourceData)

    def delete_resource(self, resourceId: str):
        """Gets stuff."""
        return self._delete_detailed("resource", resourceId)

    def get_projects(self) -> ProjectList:
        """Gets stuff."""
        return parse._projectlist(self._get_all("project"))

    def get_project_details(self, projectId: str) -> ProjectDetails:
        """Gets stuff."""
        return parse._projectdetails(self._get_detailed("project", projectId))

    def create_project(self, ProjectData: ProjectDetails):
        """Gets stuff."""
        return self._create_detailed("project", ProjectData)

    def modify_project(self, projectId: str, ProjectData: ProjectDetails):
        """Gets stuff."""
        return self._modify_detailed("project", projectId, ProjectData)

    def delete_project(self, projectId: str):
        """Gets stuff."""
        return self._delete_detailed("project", projectId)
