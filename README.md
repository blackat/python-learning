# Python - Theory and Exercises

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Run tests

```bash
pytest
```

## Run with coverage

```bash
pytest --cov=myproject --cov-report=html
```