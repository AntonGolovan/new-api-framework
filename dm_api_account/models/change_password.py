from pydantic import BaseModel, Field, ConfigDict


class ChangePassword(BaseModel):
    """
    Модель данных для изменения пароля пользователя.
    
    Содержит данные, необходимые для смены пароля пользователя,
    включая токен активации и старый/новый пароли.
    """
    model_config = ConfigDict(extra='forbid')
    
    login: str = Field(..., description='Логин пользователя')
    token: str = Field(..., description='Токен активации')
    oldPassword: str = Field(..., description='Старый пароль', alias='oldPassword')
    newPassword: str = Field(..., description='Новый пароль', alias='newPassword')