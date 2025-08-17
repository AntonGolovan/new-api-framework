from pydantic import BaseModel, Field, ConfigDict


class Registration(BaseModel):
    """
    Модель данных для регистрации нового пользователя.
    
    Содержит обязательные поля для создания нового аккаунта в системе.
    """
    model_config = ConfigDict(extra='forbid')
    
    login: str = Field(..., description='Логин пользователя')
    password: str = Field(..., description='Пароль пользователя')
    email: str = Field(..., description='Email пользователя')