import pytest

from building_blocks.domain.domain_error import DomainError


class TestDomainError:
    def test_domain_error_when_raised_is_an_exception(self):
        with pytest.raises(DomainError):
            raise DomainError("This is a domain error")
