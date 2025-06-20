import datetime

import pytest

from taskflow_primitives.infrastructure.parsers.iso8601_due_date_parser import (
    ISO8601DueDateParser,
)


class TestISO8601DueDateParser:
    def test_parse_when_valid_iso_8601_then_date(self):
        parser = ISO8601DueDateParser()

        # Test with a valid ISO 8601 date
        result = parser.parse("2023-10-01")

        expected_date = datetime.date(2023, 10, 1)
        assert result == expected_date

    def test_parse_when_invalid_iso_8601_string_then_raises_value_error(self):
        parser = ISO8601DueDateParser()

        # Test with an invalid ISO 8601 date
        with pytest.raises(ValueError, match="Invalid ISO 8601 date format"):
            parser.parse("invalid-date")

    def test_parse_when_empty_string_then_raises_value_error(self):
        parser = ISO8601DueDateParser()

        # Test with an empty string
        with pytest.raises(ValueError, match="Invalid ISO 8601 date format"):
            parser.parse("")

    def test_parse_when_none_then_raises_value_error(self):
        parser = ISO8601DueDateParser()

        # Test with None
        with pytest.raises(TypeError):
            parser.parse(None)
