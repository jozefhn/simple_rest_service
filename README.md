# Simple REST service

Tech stack:
* FastAPI
* Sqlmodel
* Pydantic
* sqlite

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
pip install -r requirements.txt
```

### Run dev server

With active venv run:

```bash
fastapi dev app/main.py
```

Now you can use:
* rest api: http://localhost:8000
* automatic interactive documentation with Swagger UI: http://localhost:8000/docs


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


## Reference
Used template (with principle "you get to use what you need and understand"):
https://github.com/fastapi/full-stack-fastapi-template
