import pytest

from building_blocks.domain.errors import DomainValidationError


class TestDomainValidationError:
    def test_init_when_message_then_message_is_set(self):
        message = "This is a validation error."

        error = DomainValidationError(message=message)

        assert error.message == message

    def test_init_when_no_context_then_context_is_empty(self):
        message = "This is a validation error."

        error = DomainValidationError(message=message)

        assert error.context == {}

    def test_init_when_context_from_wrong_type_then_raises_type_error(self):
        message = "This is a validation error."

        with pytest.raises(TypeError):
            DomainValidationError(message, context="not a dict")  # type: ignore

    def test_str_representation(self):
        error_message = "This is a validation error."

        error = DomainValidationError(message=error_message, context={"key": "value"})

        assert str(error) == f"{error_message} | Context: {{'key': 'value'}}"

    def test_str_representation_without_context(self):
        error_message = "This is a validation error."

        error = DomainValidationError(message=error_message)

        assert str(error) == error_message
