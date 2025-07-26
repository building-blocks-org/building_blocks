from dataclasses import dataclass


@dataclass(frozen=True)
class TokenAlgorithm:
    """
    Represents a token algorithm used for signing and verifying tokens.
    This class is used to define the type of algorithm being used.
    """

    HS256 = "HS256"
    RS256 = "RS256"
    ES256 = "ES256"
    PS256 = "PS256"
    NONE = "none"
