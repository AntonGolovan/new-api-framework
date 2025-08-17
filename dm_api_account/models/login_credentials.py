from pydantic import BaseModel, Field, ConfigDict


class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='логин')
    password: str = Field(..., description='пароль')
    remember_me: bool = Field(..., description='Запомни меня', serialization_alias='rememberMe')