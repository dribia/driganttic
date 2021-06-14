# Contribute

<p style="text-align: center; padding-bottom: 1rem;">
    <a href="https://github.com/Dribia/driganttic">
        <img 
            src="../img/logo_dribia_blau_cropped.png" 
            alt="driganttic" 
            style="display: block; margin-left: auto; margin-right: auto; width: 40%;"
        >
    </a>
</p>

<p style="text-align: center;">
    <em>Contributions to Dribia libraries are always welcome!</em>
</p>

## Mantainers
*driganttic* is maintained by:

* Oleguer Sagarra Pascual - <ula@dribia.com>

## Source code
In order to contribute, the first step is to clone yourself the code:
[repository](https://github.com/Dribia/driganttic):
```shell
git clone git@github.com:Dribia/driganttic.git
```
Then, you can step into the project's root and, assuming that you have both [Poetry](https://python-poetry.org/) and 
[pre-commit](https://pre-commit.com/) installed, run:
```shell
poetry install
pre-commit install
```

## Contribute
Now you should be ready to start coding your contribution to the project. Just remember the following rules:

* Use [Black](https://github.com/psf/black) for code linting and the PEP they respect.
* Branch the repo following an apropriate [branching protocol](https://nvie.com/posts/a-successful-git-branching-model/).
* Always merge your contributions via pull requests, setting the maintainers as reviewers.
* When working on a `release`, follow the [symver protocol](https://semver.org/).

Happy coding!
