from pydantic import BaseModel, Field, ConfigDict


class ChangeEmail(BaseModel):
    """
    Модель данных для изменения email пользователя.
    
    Содержит данные, необходимые для смены email-адреса пользователя.
    """
    model_config = ConfigDict(extra='forbid')
    
    login: str = Field(..., description='Логин пользователя')
    password: str = Field(..., description='Пароль пользователя')
    email: str = Field(..., description='Новый email пользователя')