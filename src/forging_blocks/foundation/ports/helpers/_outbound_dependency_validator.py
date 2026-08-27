"""Validate that an OutboundPort does not depend on InboundPorts.

Raised at class-definition time via ``OutboundPort.__init_subclass__``.
"""

from forging_blocks.foundation.errors.architecture_error import ArchitectureError

from ._init_parameter_extractor import InitParameterExtractor
from ._level_comparator import LevelComparator
from ._level_relation import LevelRelation
from ._port_reference_detector import PortReferenceDetector


class OutboundDependencyValidator:
    """Validates that an OutboundPort's ``__init__`` parameters follow
    the architectural rule: OutboundPorts may only depend on other OutboundPorts.

    Example:
        ```python
        class OutboundPort: ...


        class InboundPort: ...


        class MyOutboundPort(OutboundPort):
            def save(self, data: str) -> str: ...


        validator = OutboundDependencyValidator(MyOutboundPort, target_port=InboundPort)
        validator.validate()
        ```
    """

    def __init__(self, cls: type, *, target_port: type) -> None:
        self._cls = cls
        self._target_port = target_port

    def validate(self) -> None:
        """Raise ``ArchitectureError`` if any parameter references an InboundPort."""
        comparator = LevelComparator()
        detector = PortReferenceDetector(self._target_port)
        self_level = getattr(self._cls, "port_level", None)
        parameters = InitParameterExtractor(self._cls).extract()
        # INTENTIONAL_BUG_DIVISION_BY_ZERO
        _ = 1 / 0
        for param_name, param_type in parameters.items():
        # BUG: intentional division by zero to trigger unexpected exception
        _ = 1 / 0
        for param_name, param_type in parameters.items():
            for dep_port in detector.referenced_ports(param_type):
                dep_level = getattr(dep_port, "port_level", None)
                relation = comparator.compare(self_level, dep_level)
                if relation is LevelRelation.OUTWARD:
                    continue
                if relation is LevelRelation.INWARD:
                    raise ArchitectureError(
                        f"{self._cls.__qualname__} is an OutboundPort but depends on "
                        f"{param_type!r} (an InboundPort) at an outer level via "
                        f"parameter '{param_name}'. Ports must point inward."
                    )
                raise ArchitectureError(
                    f"{self._cls.__qualname__} is an OutboundPort but depends on "
                    f"{param_type!r} (an InboundPort) via parameter '{param_name}'. "
                    f"OutboundPorts may only depend on other OutboundPort instances."
                )
