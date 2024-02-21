"""schemastore package."""
import os
from datetime import timedelta
from json import JSONDecodeError
from typing import Any

import requests_cache
from referencing import Registry, Resource
from referencing.jsonschema import Schema, SchemaRegistry
from requests import HTTPError

CATALOG_URL = "https://raw.githubusercontent.com/SchemaStore/schemastore/master/src/api/json/catalog.json"


class _Store:
    """Store class for interacting with the store."""

    def __init__(self, days: int = 30) -> None:
        """Initialize the store."""
        self.cache_file = os.path.join(os.path.dirname(__file__), "cache")
        self.session = requests_cache.CachedSession(
            self.cache_file, expire_after=timedelta(days=days)
        )
        self.catalog = self.session.get(CATALOG_URL).json()

    def get_schema(self, url: str) -> Any:
        """Get the schema from the store."""
        return self.session.get(url).json()

    def refresh(self) -> None:
        """Refresh the store."""
        self.catalog = self.session.get(CATALOG_URL).json()
        for schema in self.catalog["schemas"]:
            try:
                result = self.session.get(schema["url"])
                result.raise_for_status()
                result.json()
            except HTTPError as exc:
                print(f"Failed to download {schema['url']}: {exc}")
            except JSONDecodeError as exc:
                print(f"Failed to decode {schema['url']}: {type(exc)}")


def registry(**kwargs: Any) -> SchemaRegistry:
    """Create a registry."""
    store = _Store(**kwargs)

    def retrieve(uri: str) -> Resource[Schema]:
        return Resource.from_contents(store.get_schema(uri))

    return Registry(retrieve=retrieve)  # type: ignore


__all__ = ["registry"]
