from forging_blocks.domain.specification.base import Specification
from forging_blocks.domain.specification.composable import ComposableSpecification


class NotSpecification[T](ComposableSpecification[T]):
    """Logical NOT of a specification.

    Satisfied if and only if the wrapped specification is NOT satisfied.

    Inherits composition operators from ``ComposableSpecification`` so that the
    result of a negation is itself composable (e.g. ``(~a) & b``).

    Example:
        ```python
        from forging_blocks.domain.specification.logical_operators.not_specification import (
            NotSpecification,
        )
        from forging_blocks.domain.specification.expression import (
            ExpressionSpecification,
        )

        is_banned = ExpressionSpecification(lambda u: u.status == "banned", "is_banned")

        # Direct construction
        not_banned = NotSpecification(is_banned)
        # Equivalent via operator
        same = ~is_banned  # Produces a NotSpecification
        ```
    """

    __slots__ = ("_wrapped_specification",)

    def __init__(self, wrapped: Specification[T]) -> None:
        self._wrapped_specification = wrapped

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._wrapped_specification.is_satisfied_by(candidate)

    def __repr__(self) -> str:
        return f"NotSpecification({self._wrapped_specification!r})"
