
## Poetry
We recommend to use [**Poetry**](https://python-poetry.org/) for dependency management.

### Add the dependency
Once Poetry has been configured with the *dripy* repository you can add your *driganttic* dependency.

At this moment, Poetry does not have a way to do this using only the CLI. You still have to 
configure the *dripy* source manually on your `pyproject.toml` file, by adding the following section:

```toml
[[tool.poetry.source]]
name = "dripy"
url = "https://dripy.dribia.dev"
secondary = true
```

Now you can add `driganttic` as a dependency of your project as you would do with any other 
python package:
```shell
poetry add driganttic
```
