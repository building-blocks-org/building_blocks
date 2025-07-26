from dataclasses import dataclass


@dataclass(frozen=True)
class TokenClaims:
    user_id: str  # sub
    expires_at: int  # exp
    email: str  # user email
