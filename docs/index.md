<p style="text-align: center; padding-bottom: 1rem;">
    <a href="https://dribia.github.io/driganttic/">
        <img 
            src="img/logo_dribia_blau_cropped.png" 
            alt="driganttic" 
            style="display: block; margin-left: auto; margin-right: auto; width: 40%;"
        >
    </a>
</p>

<p style="text-align: center">
    <a href="https://github.com/psf/black" target="_blank">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
    </a>
</p>

<p style="text-align: center;">
    <em>Ganttic API client</em>
</p>

---

**Documentation**: <a href="https://dribia.github.io/driganttic/" target="_blank">https://dribia.github.io/driganttic/</a>

**Source Code**: <a href="https://github.com/Dribia/driganttic" target="_blank">
https://github.com/Dribia/driganttic</a>

---

API REST [Ganttic](https://www.ganttic.com/helpdesk/api) client for python.

## Key features

* Client simple programmatic access to Ganttic API Rest
* Pydantic responses


!!! warning
    Some relevant features are missing, because they were not relevant for our usecase.
        
    * It only implements GET methods
    * It does not implement all fields of Tasks, Resources and Projects as they were not needed to us
    * It does not implement custom field fetchers for either texts or users


## Example

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
All results are [pydantic models](https://pydantic-docs.helpmanual.io/) already formatted with the interesting fields.
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

!!! tip
    Make sure to pass as dictionaries the pairs ganttic names vs pydantic names in 
    the appropriate order.

## License

This software is licensed under the MIT license.

MIT License

Copyright (c) 2021 Dribia Data Research

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## TODOs

- [ ] Make optional to exhaust pages (now by default it exhausts the pages)
- [ ] Implement good testing, in line using TestClient from [Starlette](https://fastapi.tiangolo.com/tutorial/testing/) by mocking the API response.
- [ ] Implement modify, create and delete methods
- [ ] Implement custom data types texts and users
