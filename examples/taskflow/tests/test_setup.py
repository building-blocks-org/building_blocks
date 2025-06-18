"""Test that the taskflow example is properly set up."""


def test_building_blocks_import():
    """Test that we can import building-blocks components."""
    from building_blocks.domain import Entity, Event, ValueObject

    assert Entity is not None
    assert ValueObject is not None
    assert Event is not None


def test_project_import():
    """Test that we can import taskflow."""
    import taskflow

    assert taskflow.__version__ == "0.1.0"
    assert taskflow.__author__ == "Glauber Brennon"


class TestProjectStructure:
    """Test that the project structure is correct."""

    def test_can_import_domain_layer(self):
        """Test domain layer package structure."""

    def test_can_import_application_layer(self):
        """Test application layer package structure."""

    def test_can_import_infrastructure_layer(self):
        """Test infrastructure layer package structure."""

    def test_can_import_presentation_layer(self):
        """Test presentation layer package structure."""
