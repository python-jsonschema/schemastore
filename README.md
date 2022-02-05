# schemastorepy

Contains all JSON Schemas from [schemastore.org](https://schemastore.org)
catalog so you can make use of them without needing internet access.

## How to use

```python
from schemastore import Store

store = Store(days=30)
my_schema_json = store.get('http://...') # <-- no network access happens
```

The `days` parameter is optional and defaults to 30, which means that after
this it will start checking if the locally cached schema is up to date and
refresh it it needed. `store.catalog` would contain
the content of the catalog itself.

## Stats

- Over 500 JSON Schemas in the catalog
- ~2.5Mib package size
- ~30Mib installed size
