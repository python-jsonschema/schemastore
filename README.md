# schemastore.py

A collection of all JSON Schemas from the [schemastore.org](https://schemastore.org) catalog, installable so they may be used without internet access.

## Installation

Use your favorite package manager, e.g. via:

    $ uv pip install schemastore

or

    $ pip install schemastore

## Usage

Schemas are made usable as a [`referencing.Registry`](https://referencing.readthedocs.io/en/stable/api/#referencing.Registry).
It is available as:


```python
import schemastore
registry = schemastore.registry()
```

and use any of the API from the aforementioned referencing package to make use of the schemas, such as:

```python
print(registry.get_or_retrieve("https://json.schemastore.org/github-action.json").value)

```

though more typically you will use the registry alongside a JSON Schema validator such as those provided by the [`jsonschema` library](https://python-jsonschema.readthedocs.io/):

```python
import jsonschema
import schemastore


# Validate whether the string "foo" is a valid GitHub actions workflow (it is not.)
jsonschema.validate(
    '"foo"',
    {"$ref": "https://json.schemastore.org/github-action.json"},
    registry=schemastore.registry(),
)
```
