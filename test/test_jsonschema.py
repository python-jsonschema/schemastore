"""Test module."""
import schemastore


def test_one() -> None:
    """Test one."""
    registry = schemastore.registry()
    assert registry is not None
