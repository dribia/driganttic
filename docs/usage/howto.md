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

!!! "Things to note"
    1. The client will automatically exhaust all the pagination if you use the `get_something` method (not the `get_something_details`).
    2. The client returns pydantic models, where only the relevant data has been kept.

!!! warning
    The library has some limitations

    Mostly that with ill formatted ganttic tasks, (a.k.a.) earlier than 2021, *it might not work*.