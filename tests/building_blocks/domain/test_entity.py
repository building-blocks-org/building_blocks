from building_blocks.domain.entity import Entity


class FakeEntity(Entity[str]):
    """
    A fake entity for testing purposes.

    This class is used to create a mock entity with a string identifier.
    It inherits from the Entity class and implements the required methods.
    """

    def __init__(self, id: str):
        super().__init__(id)


class TestEntity:
    def test_eq_when_another_entity_with_the_same_id_then_true(self):
        entity1 = FakeEntity("123")
        entity2 = FakeEntity("123")

        result = entity1 == entity2

        expected_result = True
        assert result is expected_result, "Entities with the same ID should be equal"

    def test_eq_when_another_entity_with_different_id_then_false(self):
        entity1 = FakeEntity("123")
        entity2 = FakeEntity("456")

        result = entity1 == entity2

        expected_result = False
        result_assertion = result is expected_result
        assert result_assertion, "Entities with different IDs should not be equal"

    def test_eq_when_another_object_then_false(self):
        entity = FakeEntity("123")
        other_object = object()

        result = entity == other_object

        expected_result = False
        result_assertion = result is expected_result
        assert result_assertion, "Entity should not be equal to a non-entity object"

    def test_str_representation(self):
        entity = FakeEntity("123")

        result = str(entity)

        expected_result = "FakeEntity(id=123)"
        assert (
            result == expected_result
        ), f"String representation should be '{expected_result}'"

    def test_repr_representation(self):
        entity = FakeEntity("123")

        result = repr(entity)

        expected_result = "FakeEntity(id=123)"
        assert (
            result == expected_result
        ), f"Repr representation should be '{expected_result}'"

    def test_hash_when_id_then_hash_id(self):
        id_ = "123"
        entity = FakeEntity(id_)

        hash1 = hash(entity)

        expected_hash = hash(id_)
        assert (
            hash1 == expected_hash
        ), "Hash values should be equal for entities with the same ID"
