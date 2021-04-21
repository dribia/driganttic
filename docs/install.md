## PIP
The package can be installed with PIP from the [**dripy**](https://dripy.dribia.dev) python package repository:

```shell
pip install -i https://dripy.dribia.dev driganttic
```

The *dripy* repository is private, so this line will prompt for username / password credentials.

## Poetry
As you know, it is recommended to use [**Poetry**](https://python-poetry.org/) for dependency management.

### Configure Dripy
Poetry can be configured to use a custom repository instead of the default [pypi](https://pypi.org):

```shell
poetry config repositories.dripy https://dripy.dribia.dev
```

Since the repository is private, one has to configure the access credentials beforehand:

```shell
poetry config http-basic.dripy your_dripy_username
```

This line will prompt for your *dripy* password.

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

## Advanced Poetry

When working on a production deployment, configuring the *dripy* credentials using `poetry config` might not be
the best option.

That's why Poetry provides a way to authenticate to private repositories using environment variables.

If you have named your private repository `dripy`, by running the configuration command:

```shell
poetry config repositories.dripy https://dripy.dribia.dev
```

then by setting the following environment variables:

```shell
export POETRY_HTTP_BASIC_DRIBIA_USERNAME=<your repository username> 
export POETRY_HTTP_BASIC_DRIBIA_PASSWORD=<your repository password>
```

poetry will use them to authenticate to the private repository.
