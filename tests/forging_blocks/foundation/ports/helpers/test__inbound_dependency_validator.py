"""Tests for the InboundDependencyValidator helper.

Targets the ArchitectureError raise path (line 30).
"""

import pytest

from forging_blocks.foundation.errors.architecture_error import ArchitectureError
from forging_blocks.foundation.ports import InboundPort, OutboundPort, PortLevel
from forging_blocks.foundation.ports.helpers._inbound_dependency_validator import (
    InboundDependencyValidator,
)


class Level(PortLevel):
    OUTERMOST = 0
    MIDDLE = 1
    INNERMOST = 2


@pytest.mark.unit
class TestInboundDependencyValidator:
    def test_validate_passes_for_outbound_dependency(self) -> None:
        """Concrete InboundPort with only OutboundPort deps passes validation."""

        class Repo(OutboundPort): ...

        class UseCase(InboundPort):
            def __init__(self, repo: Repo) -> None: ...

        InboundDependencyValidator(UseCase, target_port=InboundPort).validate()

    def test_validate_raises_for_inbound_dependency(self) -> None:
        """Concrete InboundPort depending on InboundPort raises ArchitectureError (line 30)."""

        class BadInbound(InboundPort): ...

        with pytest.raises(ArchitectureError) as exc_info:

            class _(InboundPort):
                def __init__(self, dep: BadInbound) -> None: ...

        assert "_" in str(exc_info.value)

    def test_validate_passes_for_deeper_inbound_dependency(self) -> None:
        """InboundPort at an outer level depending on a deeper InboundPort passes."""

        class AppInbound(InboundPort):
            port_level = Level.INNERMOST

        class PresentationInbound(InboundPort):
            port_level = Level.OUTERMOST

            def __init__(self, app: AppInbound) -> None: ...

        InboundDependencyValidator(PresentationInbound, target_port=InboundPort).validate()

    def test_validate_raises_for_outer_inbound_dependency(self) -> None:
        """InboundPort at an outer level depending on an outer InboundPort raises."""

        class OuterInbound(InboundPort):
            port_level = Level.OUTERMOST

        with pytest.raises(ArchitectureError) as exc_info:

            class _(InboundPort):
                port_level = Level.MIDDLE

                def __init__(self, dep: OuterInbound) -> None: ...

        assert "outer" in str(exc_info.value)
