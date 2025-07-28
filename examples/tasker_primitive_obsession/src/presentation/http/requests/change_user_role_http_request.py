from pydantic import BaseModel, Field


class ChangeUserRoleHttpRequest(BaseModel):
    """
    Represents a http request to change a user's role.
    """

    new_role: str = Field(..., description="The new role to assign to the user.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "123e4567-e89b-12d3-a456-426614174000",
                    "new_role": "manager",
                },
                {
                    "user_id": "123e4567-e89b-12d3-a456-426614174001",
                    "new_role": "designer",
                },
                {
                    "user_id": "123e4567-e89b-12d3-a456-426614174000",
                    "new_role": "designer",
                },
            ]
        }
    }
