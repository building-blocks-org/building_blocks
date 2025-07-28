from typing import Union

from pydantic import BaseModel, Field


class ChangeUserRoleSucceededHttpResponse(BaseModel):
    user_id: str = Field(..., description="The ID of the user whose role was changed.")
    previous_role: str = Field(..., description="The previous role of the user.")
    new_role: str = Field(..., description="The new role assigned to the user.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "123e4567-e89b-12d3-a456-426614174000",
                    "previous_role": "designer",
                    "new_role": "manager",
                }
            ]
        }
    }


class ChangeUserRoleFailedHttpResponse(BaseModel):
    reason: str = Field(..., description="Why the role change failed.")
    code: str = Field(..., description="Error code for client-side handling.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"reason": "User not found.", "code": "USER_NOT_FOUND"},
                {"reason": "Role is not permitted.", "code": "ROLE_NOT_ALLOWED"},
            ]
        }
    }


ChangeUserRoleHttpResponse = Union[
    ChangeUserRoleSucceededHttpResponse, ChangeUserRoleFailedHttpResponse
]
