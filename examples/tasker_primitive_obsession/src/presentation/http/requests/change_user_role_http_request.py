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
                    "new_role": "manager",
                },
                {
                    "new_role": "designer",
                },
                {
                    "new_role": "engineer",
                },
                {
                    "new_role": "admin",
                },
            ]
        }
    }
