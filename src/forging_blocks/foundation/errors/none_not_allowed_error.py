"""Error indicating that a None value was provided where it is not allowed."""
from collections.abc import Mapping


from forging_blocks.foundation.errors.error import Error


class NoneNotAllowedError[MetadataType: Mapping[str, object] = dict[str, object]](Error[MetadataType]):
    """Error indicating that a None value was provided where it is not allowed."""
