

# driganttic

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
```python

class TaskDetails(FetcherDetails):
    """Task List schema."""

    # could be holidays
    projectId: Optional[str]
    resources: List[str]
    start: datetime.datetime
    end: datetime.datetime
    utilizationPercent: Optional[float]

    # Define here your custom fields
    my_custom_pydantic_name: Optional[str]
```
2. Head to `config/config.yaml` and add your declared custom fields under the dict 
   for the relevant fetcher (task, project or resource) and type (number, date, listvalue, user or text)

```yaml
custom_fields:
  tasks:
    listValues:
       my_custom_ganttic_name: my_pydnatic_name
    numbers:
    dates:
  projects:
    listValues:
    numbers:
    dates:
  resources:
    listValues:
    numbers:
    dates:
```


## License

This package is licensed under the MIT license, see `LICENSE.md`.

## TODOs

- [ ] Make optional to exhaust pages (now by default it exhausts the pages)
- [ ] Implement good testing, in line using TestClient from [Starlette](https://fastapi.tiangolo.com/tutorial/testing/) by mocking the API response.
- [ ] Implement modify, create and delete methods
- [ ] Implement custom data types texts and users
