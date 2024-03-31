"""schemastore package."""

from datetime import timedelta
from json import JSONDecodeError
from pathlib import Path
from sys import stderr
from typing import Any

from referencing import Registry, Resource
from referencing.jsonschema import SchemaRegistry, SchemaResource
from requests import HTTPError
import requests_cache

CATALOG_URL = "https://raw.githubusercontent.com/SchemaStore/schemastore/master/src/api/json/catalog.json"


class _Store:
    """Store class for interacting with the store."""

    def __init__(self, days: int = 30) -> None:
        """Initialize the store."""
        self.cache_file = Path(__file__).parent / "cache"
        self.session = requests_cache.CachedSession(
            self.cache_file,
            expire_after=timedelta(days=days),
        )
        self.catalog = self.session.get(CATALOG_URL).json()  # type: ignore[reportUnknownMemberType]

    def get_schema(self, url: str) -> Any:
        """Get the schema from the store."""
        return self.session.get(url).json()  # type: ignore[reportUnknownMemberType]

    def refresh(self) -> None:
        """Refresh the store."""
        self.catalog = self.session.get(CATALOG_URL).json()  # type: ignore[reportUnknownMemberType]
        for schema in self.catalog["schemas"]:
            url = schema["url"]
            try:
                result = self.session.get(url)  # type: ignore[reportUnknownMemberType]
                result.raise_for_status()
                result.json()
            except HTTPError as exc:
                stderr.write(f"Failed to download {url}: {exc}\n")
            except JSONDecodeError as exc:
                stderr.write(f"Failed to decode {url}: {type(exc)}\n")


def registry(**kwargs: Any) -> SchemaRegistry:
    """Create a registry."""
    store = _Store(**kwargs)

    def retrieve(uri: str) -> SchemaResource:
        return Resource.from_contents(store.get_schema(uri))  # type: ignore[reportUnknownMemberType, reportUnknownVariableType]

    return Registry(retrieve=retrieve)


__all__ = ["registry"]
