from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import (
    List,
    Optional,
    Any,
)
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class UserRole(str, Enum):
    """
    Роли пользователей в системе.
    
    Определяет права доступа и возможности пользователя в системе.
    """
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATION = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator'


class Rating(BaseModel):
    """
    Модель рейтинга пользователя.
    
    Содержит информацию о рейтинге пользователя, включая его статус
    и количественные показатели.
    """
    enabled: bool = Field(..., description='Включен ли рейтинг для пользователя')
    quality: int = Field(..., description='Качественный показатель рейтинга')
    quantity: int = Field(..., description='Количественный показатель рейтинга')


class User(BaseModel):
    """
    Модель базовой информации о пользователе.
    
    Содержит основную информацию о пользователе, включая его роли,
    рейтинг и базовые данные профиля.
    """
    login: str = Field(..., description='Логин пользователя')
    roles: List[UserRole] = Field(..., description='Список ролей пользователя')
    medium_picture_url: str = Field(None, alias='mediumPictureUrl', description='URL средней аватарки')
    small_picture_url: str = Field(None, alias='smallPictureUrl', description='URL маленькой аватарки')
    status: str = Field(None, alias='status', description='Статус пользователя')
    rating: Rating = Field(..., description='Рейтинг пользователя')
    online: datetime = Field(None, alias='online', description='Время последнего входа')
    name: str = Field(None, alias='name', description='Имя пользователя')
    location: str = Field(None, alias='location', description='Местоположение пользователя')
    registration: datetime = Field(None, alias='registration', description='Дата регистрации')


class UserEnvelope(BaseModel):
    """
    Обертка для данных пользователя.
    
    Стандартная структура ответа API, содержащая данные пользователя
    и дополнительные метаданные.
    """
    model_config = ConfigDict(extra='forbid')
    
    resource: Optional[User] = Field(None, description='Данные пользователя')
    metadata: Optional[Any] = Field(None, description='Дополнительные метаданные')