```shell
# публикация пакета
ptv patch && poetry build && poetry publish -r test-pypi
```

PYPI test

```shell
# add repository to poetry 
config poetry config repositories.test-pypi https://test.pypi.org/legacy/

# get token from https://test.pypi.org/manage/account/token/
# store token using poetry 
poetry config pypi-token.test-pypi $PYPI_TOKEN_TEST_PYPI
Note: 'test-pypi' is the name of the repository
```

PYPI Production
```shell
# get token from https://pypi.org/manage/account/token/
# store token using poetry
poetry config pypi-token.pypi $PYPI_TOKEN_PYPI
```

Bump version

```shell
poetry version prerelease
poetry version patch
```

Poetry Publish

To test

```shell
poetry publish -r test-pypi
```

To PyPi

```shell
poetry publish --build
```

#### Лит-ра
1. https://johnfraney.ca/blog/create-publish-python-package-poetry/
2. https://stackoverflow.com/questions/68882603/using-python-poetry-to-publish-to-test-pypi-org
