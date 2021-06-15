# Using the client

The use is stragihtforward from this example, where all the functionality is shown.

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

!!! tip
    Note that any of the `get_tasks`, `get_projects`, `get_resources` accept extra `kwargs` compatible with the Ganttic API GET methods.

!!! warning "Things to note"
    1. The client will automatically exhaust all the pagination if you use the `get_something` method (not the `get_something_details`).
    2. The client returns pydantic models, where only the relevant data to our usecase has been kept.

!!! warning
    The library has some limitations, mostly that the Error handling is not great for illformatted tasks

# Extending the client

Say you want to extend the client to your needs. There are some simple steps to follow.

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


!!! warning
    Custom `text` and `user` fields are currently not supported.