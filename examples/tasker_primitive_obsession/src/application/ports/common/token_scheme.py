from dataclasses import dataclass


@dataclass(frozen=True)
class TokenScheme:
    """
    Represents a token scheme used for authentication.
    This class is used to define the type of token scheme being used.
    """

    BASIC = "Basic"
    BEARER = "Bearer"
