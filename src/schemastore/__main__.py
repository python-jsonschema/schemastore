"""Main entry point module."""

from schemastore import Store


def main() -> None:
    """Refresh the cache if needed."""
    store = Store()
    print(f"Catalog has {len(store.catalog['schemas'])} schemas")
    store.refresh()
    print(f"Catalog now has {len(store.catalog['schemas'])} schemas")
