import pytest

from building_blocks.application.application_exception import ApplicationException


class TestApplicationException:
    def test_application_exception_when_raised_is_an_exception(self):
        with pytest.raises(ApplicationException):
            raise ApplicationException("This is a application exception")
