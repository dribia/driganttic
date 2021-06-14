
**Important note: This repo is still WiP, it is missing a license and the adaptation of the Docs to be fully public. For the moment, its (c) Dribia Data Research 2021 all rights reserved, soon to be MIT**.

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

**Warning: It may not works with badly formatted tasks from past usages of ganttic. Use from 2021 onwards!**

The client is very trivial to use. It implement wrappers to the main types of available calls.
```python
from driganttic import parse as dg_parse
from driganttic import client as dg_client

APIKEY = 'yourapikey'

Client = dg_client.GantticClient(APIKEY=APIKEY)
# get dictionary of custom fields
dict_of_fields = Client.Translator

print(f'Available fetchers: {dg_client.FETCHERS}')
# get all projects, tasks and resources
projects = Client.get_projects()
tasks = Client.get_tasks(timeMin = dg_parse.parse_timestamp('2021-01-01'),
                         timeMax= dg_parse.parse_timestamp('2021-04-30'))
resources = Client.get_resources()

p_id = projects.fetched_items.pop().id
t_id = tasks.fetched_items.pop().id
r_id = resources.fetched_items.pop().id
one_project = Client.get_project_details(projectId=p_id)
one_task = Client.get_task_details(taskId=t_id)
one_resource = Client.get_resource_details(resourceId=r_id)
```
All results are pydantic models already formatted with the interesting fields.
See the `fetcher.py` file in `/schemas` for details.

## Modifications

The only changes needed here are to adapt to your own custom data fields.
To do so, you need to do two things:

1. Define the relevant fields in the pydantic model definition in `schemas/fetcher.py`
2. Define the relevant parsing methods in `parse.py`, only for the fields that are not general. The rest of fields are taken care by `_fetcher` or `_fetcherDetails` methods.


## TODOs

- [ ] Better docs on limitations (pagination, custom fields, not implemented fields)
- [ ] Move all custom related field definition to configuration yaml file
- [ ] Make optional to exhaust pages (now by default it exhausts the pages)
- [ ] Implement good testing, in line using TestClient from [Starlette](https://fastapi.tiangolo.com/tutorial/testing/) by mocking the API response.
- [ ] Implement modify, create and delete methods
- [ ] Implement custom data types texts and users
