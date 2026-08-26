"""Tests for the OutboundDependencyValidator helper.

Targets the ArchitectureError raise path (line 30).
"""

import pytest

from forging_blocks.foundation.errors.architecture_error import ArchitectureError
from forging_blocks.foundation.ports import InboundPort, OutboundPort, PortLevel
from forging_blocks.foundation.ports.helpers._outbound_dependency_validator import (
    OutboundDependencyValidator,
)


class DataDepth(PortLevel):
    """Example consumer vocabulary for a persistence-facing service."""

    API = 0
    SERVICE = 1
    PERSISTENCE = 2


@pytest.mark.unit
class TestOutboundDependencyValidator:
    def test_validate_passes_for_outbound_dependency(self) -> None:
        """Concrete OutboundPort with only OutboundPort deps passes validation."""

        class Logger(OutboundPort): ...

        class Repo(OutboundPort):
            def __init__(self, logger: Logger) -> None: ...

        OutboundDependencyValidator(Repo, target_port=InboundPort).validate()

    def test_validate_raises_for_inbound_dependency(self) -> None:
        """OutboundPort depending on InboundPort raises ArchitectureError (line 30)."""

        class BadInbound(InboundPort): ...

        with pytest.raises(ArchitectureError) as exc_info:

            class _(OutboundPort):
                def __init__(self, dep: BadInbound) -> None: ...

        assert "_" in str(exc_info.value)

    def test_validate_passes_for_deeper_inbound_dependency(self) -> None:
        """OutboundPort depending on a deeper InboundPort passes (inward)."""

        class AppInbound(InboundPort):
            port_level = DataDepth.PERSISTENCE

        class MiddleOutbound(OutboundPort):
            port_level = DataDepth.SERVICE

            def __init__(self, app: AppInbound) -> None: ...

        OutboundDependencyValidator(MiddleOutbound, target_port=InboundPort).validate()

    def test_validate_raises_for_outer_inbound_dependency(self) -> None:
        """OutboundPort depending on an outer-level InboundPort raises."""

        class OuterInbound(InboundPort):
            port_level = DataDepth.API

        with pytest.raises(ArchitectureError) as exc_info:

            class _(OutboundPort):
                port_level = DataDepth.PERSISTENCE

                def __init__(self, dep: OuterInbound) -> None: ...

        assert "outer" in str(exc_info.value)
