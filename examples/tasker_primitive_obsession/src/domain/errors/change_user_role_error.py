from building_blocks.domain.errors import DomainRuleViolationError


class ChangeUserRoleError(DomainRuleViolationError):
    """
    Raised when a domain rule violation occurs during an attempt to change a user's role.
    
    This error should be used to indicate that the requested role change is not allowed
    due to specific business rules or constraints in the domain logic.
    """
    pass
