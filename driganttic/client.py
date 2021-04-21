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
from typing import Dict, Optional
import requests
import datetime

from driganttic import parse
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
        self.session = requests.Session()

    def _get_fetcher(self, fetcher_name: str, fetcher_detail_id: Optional[str] = None, **kwargs) -> Dict:
        """Gets list of the entire fetcher."""
        fetcher_endpoint = self.FETCHERS.get(fetcher_name,{}).get('endpoint')
        if fetcher_endpoint is None:
            raise NotImplementedError('Fectcher not implemented')
        if fetcher_detail_id is not None:
            # need to erase the final 's'
            fetcher_endpoint = fetcher_endpoint[:-1] + '/' + str(fetcher_detail_id)
        headers = {"Accept": "application/json"}
        req_string = self.ENDPOINT + '/' + fetcher_endpoint
        kwargs['token'] = self.APIKEY
        with self.session as session:
            # TODO: Implement exception catching
            return session.get(req_string, params = kwargs, headers = headers)


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

    def get_tasks(self, timeMin: datetime.datetime, timeMax: datetime.datetime ,**kwargs) -> TaskList:
        """Gets stuff."""
        return parse._tasklist(self._get_fetcher("task", timeMin=timeMin.strftime('%Y-%m-%d %H:%M'),
                                                 timeMax=timeMax.strftime('%Y-%m-%d %H:%M'), **kwargs))

    def get_task_details(self, taskId: str, **kwargs) -> FetcherDetails:
        """Gets stuff."""
        return parse._taskdetails(self._get_fetcher("task", fetcher_detail_id = taskId, **kwargs))

    def create_task(self, TaskData: TaskDetails):
        """Creates stuff."""
        return self._create_detailed("task", TaskData)

    def modify_task(self, taskId: str, TaskData: TaskDetails):
        """Gets stuff."""
        return self._modify_detailed("task", taskId, TaskData)

    def delete_task(self, taskId: str):
        """Gets stuff."""
        return self._delete_detailed("task", taskId)

    def get_resources(self,**kwargs) -> ResourceList:
        """Gets stuff."""
        return parse._resourcelist(self._get_fetcher("resource", **kwargs))

    def get_resource_details(self, resourceId: str, **kwargs) -> ResourceDetails:
        """Gets stuff."""
        return parse._resourcedetails(self._get_fetcher("resource", fetcher_detail_id=resourceId, **kwargs))

    def create_resource(self, ResourceData: ResourceDetails):
        """Gets stuff."""
        return self._create_detailed("resource", ResourceData)

    def modify_resource(self, resourceId: str, ResourceData: ResourceDetails):
        """Gets stuff."""
        return self._modify_detailed("resource", resourceId, ResourceData)

    def delete_resource(self, resourceId: str):
        """Gets stuff."""
        return self._delete_detailed("resource", resourceId)

    def get_projects(self, **kwargs) -> ProjectList:
        """Gets stuff."""
        return parse._projectlist(self._get_fetcher("project", **kwargs))

    def get_project_details(self, projectId: str, **kwargs) -> ProjectDetails:
        """Gets stuff."""
        return parse._projectdetails(self._get_fetcher("project", fetcher_detail_id=projectId, **kwargs))

    def create_project(self, ProjectData: ProjectDetails):
        """Gets stuff."""
        return self._create_detailed("project", ProjectData)

    def modify_project(self, projectId: str, ProjectData: ProjectDetails):
        """Gets stuff."""
        return self._modify_detailed("project", projectId, ProjectData)

    def delete_project(self, projectId: str):
        """Gets stuff."""
        return self._delete_detailed("project", projectId)
