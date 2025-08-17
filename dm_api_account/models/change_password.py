from pydantic import BaseModel, Field, ConfigDict


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='логин')
    token: str = Field(..., description='token')
    oldPassword: str = Field(..., description='старый пароль', alias='oldPassword')
    newPassword: str = Field(..., description='новый пароль', alias='newPassword')