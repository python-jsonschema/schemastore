import schemastore


def test_registry_creation():
    assert schemastore.registry() is not None
