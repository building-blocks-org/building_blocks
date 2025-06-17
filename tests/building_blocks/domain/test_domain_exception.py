import pytest

from building_blocks.domain.domain_exception import DomainException


class TestDomainException:
    def test_domain_exception_when_raised_is_an_exception(self):
        with pytest.raises(DomainException):
            raise DomainException("This is a domain exception")
