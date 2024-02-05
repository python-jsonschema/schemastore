"""Test module."""

from schemastore import Store


def test_one() -> None:
    """Test one."""
    store = Store()
    assert store.catalog is not None
