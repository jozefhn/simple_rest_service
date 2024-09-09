# Simple REST service

## Requirements

* [Poetry] for Python package and environment management (optional)
* [Docker compose] for Docker container (optional)

## Local pyenv development

### Install dependencies

Use poetry:

```bash
poetry install
```

or alternatively use requirements.txt

```bash
pip install requirements.txt
```

### Run dev server

With active venv run:

```bash
fastapi dev app/main.py
```

### Dev tools

Install pre-commit hooks [optional]

```bash
pre-commit install
```


## Docker

Use docker compose (from within main directory):

```bash
docker compose up
```
