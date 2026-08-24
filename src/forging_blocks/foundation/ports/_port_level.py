"""Ordered base for port depth, letting consumers define their own layers.

The library does not ship preset layer names. Consumers subclass
``PortLevel`` and add members whose integer value represents relative depth:
a larger value is a deeper (more inward) layer. ``port_level`` on a port
holds such a member (or a plain ``int``); higher reported value = deeper.
"""

from enum import IntEnum


class PortLevel(IntEnum):
    """Base ordering for a consumer-declared port depth.

    Subclass it with your own named members; the greater the integer, the
    deeper (more inward) the layer relative to the application core. The
    library enforces only this integer ordering — it never relies on member
    names, so any vocabulary (api/service/domain, web/app/data, ...) fits.

    Example:
        ```python
        class ProjectLevel(PortLevel):
            API = 0
            ORCHESTRATION = 1
            ENTITY = 2
        ```
    """
