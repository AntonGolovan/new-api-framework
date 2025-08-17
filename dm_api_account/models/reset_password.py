from pydantic import BaseModel, Field, ConfigDict


class ResetPassword(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='логин')
    email: str = Field(..., description='Email')