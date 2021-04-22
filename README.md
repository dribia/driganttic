# driganttic

[![Build](https://bitbucket.org/dribia_team/badges/downloads/status_driganttic.svg)](https://bitbucket.org/dribia_team/driganttic/addon/pipelines/home)
[![codecov](https://bitbucket.org/dribia_team/badges/downloads/coverage_driganttic.svg)](https://bitbucket.org/dribia_team/driganttic/addon/pipelines/home)
[![DriPy](https://bitbucket.org/dribia_team/badges/downloads/version_driganttic.svg)](https://dripy.dribia.dev/packages/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*Ganttic API client*

---

**Documentation**: [https://docs.dribia.dev/driganttic](https://docs.dribia.dev/driganttic)

**Source Code**: [https://bitbucket.org/dribia_team/driganttic](https://bitbucket.org/dribia_team/driganttic)

---

API REST [Ganttic](https://www.ganttic.com/helpdesk/api) client for python.

## Key features

* Client simple programmatic access to Ganttic API Rest
* Pydantic responses

## Example

The client is very trivial to use. It implement wrappers to the main types of available calls.
```python
from driganttic.client import GantticClient
import driganttic

APIKEY = 'yourapikey'

Client = GantticClient(APIKEY=APIKEY)

print(f'Available fetchers: {driganttic.client.FETCHERS}')
# get all projects, tasks and resources
projects = Client.get_projects()
tasks = Client.get_tasks(timeMin =, timeMax=)
resources = Client.get_resources()

one_project = Client.get_project_details(projectId='23932')
one_task = Client.get_task_details(projectId='23932')
one_resource = Client.get_resource_details(projectId='23932')
```
All results are pydantic models already formatted with the interesting fields.

## TODOs

- [x] get endpoints
- [x] Fix tests on details
- [ ] Implement pydantic parsers
- [ ] Implement modify, create and delete methods