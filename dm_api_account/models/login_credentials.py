from pydantic import BaseModel, Field, ConfigDict


class LoginCredentials(BaseModel):
    """
    Модель данных для аутентификации пользователя.
    
    Содержит учетные данные пользователя для входа в систему.
    """
    model_config = ConfigDict(extra='forbid')
    
    login: str = Field(..., description='Логин пользователя')
    password: str = Field(..., description='Пароль пользователя')
    remember_me: bool = Field(..., description='Флаг "Запомнить меня"', serialization_alias='rememberMe')