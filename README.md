

# driganttic

[![Build](https://bitbucket.org/dribia_team/badges/downloads/status_driganttic.svg)](https://bitbucket.org/dribia_team/driganttic/addon/pipelines/home)
[![codecov](https://bitbucket.org/dribia_team/badges/downloads/coverage_driganttic.svg)](https://bitbucket.org/dribia_team/driganttic/addon/pipelines/home)
[![DriPy](https://bitbucket.org/dribia_team/badges/downloads/version_driganttic.svg)](https://dripy.dribia.dev/packages/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*Ganttic API client*

---

**Documentation**: [https://dribia.github.io/driganttic/](https://dribia.github.io/driganttic/)

**Source Code**: [https://github.com/Dribia/driganttic](https://github.com/Dribia/driganttic)

---

API REST [Ganttic](https://www.ganttic.com/helpdesk/api) client for python.

## Key features

* Client simple programmatic access to Ganttic API Rest
* Pydantic responses

## Missing features

* It only implements GET methods
* It does not implement all fields of Tasks, Resources and Projects as they were not needed to us
* It does not implement custom field fetchers for either texts or users

## Example

The client is very trivial to use. It implements wrappers to the main types of available calls.
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
2. Head to `parse.py` and add your declared custom fields under the `CUSTOM_FIELDS` dict 
   for the relevant fetcher (task, project or resource) and type (number, date, listvalue, user or text)

```python
CUSTOM_FIELDS = {
    'task' : {
        # define pairs of name in the dict, one for the pydantic and one for the ganttic name
        'listValues' : {'my_ganttic_custom_name':¡'my_pydantic_name'},
        'numbers': {},
        'dates': {},
    },
    'resource' : {
        'listValues' : {},
        'numbers': {},
        'dates': {},
    },
    'project' : {
        'listValues' : {},
        'numbers': {},
        'dates': {},
    },
}
```


## TODOs

- [ ] Better docs on limitations (pagination, custom fields, not implemented fields)
- [ ] Move all custom related field definition to configuration yaml file
- [ ] Make optional to exhaust pages (now by default it exhausts the pages)
- [ ] Implement good testing, in line using TestClient from [Starlette](https://fastapi.tiangolo.com/tutorial/testing/) by mocking the API response.
- [ ] Implement modify, create and delete methods
- [ ] Implement custom data types texts and users
