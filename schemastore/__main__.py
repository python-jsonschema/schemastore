"""
Refresh the cache.
"""

from sys import stdout

from schemastore import _Store  # type: ignore[reportPrivateUsage]


def main() -> None:
    """Refresh the cache if needed."""
    store = _Store()
    stdout.write(f"Catalog has {len(store.catalog['schemas'])} schemas\n")
    store.refresh()
    stdout.write(f"Catalog now has {len(store.catalog['schemas'])} schemas\n")
