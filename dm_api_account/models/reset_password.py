from pydantic import BaseModel, Field, ConfigDict


class ResetPassword(BaseModel):
    """
    Модель данных для сброса пароля пользователя.
    
    Содержит данные, необходимые для инициации процесса сброса пароля.
    """
    model_config = ConfigDict(extra='forbid')
    
    login: str = Field(..., description='Логин пользователя')
    email: str = Field(..., description='Email пользователя для отправки инструкций')