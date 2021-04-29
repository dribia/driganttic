<p style="text-align: center; padding-bottom: 1rem;">
    <a href="https://docs.dribia.dev">
        <img 
            src="img/logo_dribia_blau_cropped.png" 
            alt="driganttic" 
            style="display: block; margin-left: auto; margin-right: auto; width: 40%;"
        >
    </a>
</p>

<p style="text-align: center">
    <a href="https://bitbucket.org/dribia_team/driganttic/addon/pipelines/home" target="_blank">
        <img src="https://bitbucket.org/dribia_team/badges/downloads/status_driganttic.svg" alt="Build">
    </a>
    <a href="https://bitbucket.org/dribia_team/driganttic/addon/pipelines/home" target="_blank">
        <img src="https://bitbucket.org/dribia_team/badges/downloads/coverage_driganttic.svg" alt="Coverage">
    </a>
    <a href="https://dripy.dribia.dev/packages/" target="_blank">
        <img src="https://bitbucket.org/dribia_team/badges/downloads/version_driganttic.svg" alt="DriPy">
    </a>
    <a href="https://github.com/psf/black" target="_blank">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
    </a>
</p>

<p style="text-align: center;">
    <em>Ganttic API client</em>
</p>

---

**Documentation**: <a href="https://docs.dribia.dev/driganttic" target="_blank">https://docs.dribia.dev/driganttic</a>

**Source Code**: <a href="https://bitbucket.org/dribia_team/driganttic" target="_blank">
https://bitbucket.org/dribia_team/driganttic</a>

---

API REST [Ganttic](https://www.ganttic.com/helpdesk/api) client for python.

## Key features

* Client simple programmatic access to Ganttic API Rest
* Pydantic responses

## Example

!!! danger
    It may not work with badly formatted tasks from past usages of ganttic. Use from 2021 onwards!

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

- [ ] Implement modify, create and delete methods
