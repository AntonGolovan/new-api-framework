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

from dm_api_account.models.user_envelope import (
    Rating,
    UserRole,
)


class ColorSchema(str, Enum):
    """
    Цветовые схемы интерфейса пользователя.
    
    Определяет визуальное оформление интерфейса для пользователя.
    """
    MODERN = 'Modern'
    PALE = 'Pale'
    CLASSIC = 'Classic'
    CLASSIC_PALE = 'ClassicPale'
    NIGHT = 'Night'


class BbParseMode(str, Enum):
    """
    Режимы парсинга BB-кода.
    
    Определяет способ обработки BB-кода в текстовом контенте.
    """
    COMMON = 'Common'
    INFO = 'Info'
    POST = 'Post'
    CHAT = 'Chat'


class InfoBbText(BaseModel):
    """
    Модель BB-текста с информацией.
    
    Содержит текст и режим его парсинга.
    """
    value: Optional[str] = Field(None, description='Текстовое содержимое')
    parse_mode: Optional[BbParseMode] = Field(None, description='Режим парсинга BB-кода')


class PagingSettings(BaseModel):
    """
    Настройки пагинации для различных типов контента.
    
    Определяет количество элементов на странице для разных разделов.
    """
    model_config = ConfigDict(extra='forbid')
    
    posts_per_page: int = Field(..., alias='postsPerPage', description='Количество постов на странице')
    comments_per_page: int = Field(..., alias='commentsPerPage', description='Количество комментариев на странице')
    topics_per_page: int = Field(..., alias='topicsPerPage', description='Количество тем на странице')
    messages_per_page: int = Field(..., alias='messagesPerPage', description='Количество сообщений на странице')
    entities_per_page: int = Field(..., alias='entitiesPerPage', description='Количество сущностей на странице')


class UserSettings(BaseModel):
    """
    Настройки пользователя.
    
    Содержит персональные настройки пользователя, включая цветовую схему,
    приветственное сообщение и настройки пагинации.
    """
    model_config = ConfigDict(extra='forbid')
    
    color_schema: ColorSchema = Field(None, alias='colorSchema', description='Цветовая схема интерфейса')
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage', description='Приветственное сообщение')
    paging: PagingSettings = Field(None, description='Настройки пагинации')


class UserDetails(BaseModel):
    """
    Детальная информация о пользователе.
    
    Расширенная модель пользователя, содержащая дополнительную информацию
    о профиле, настройках и контактных данных.
    """
    model_config = ConfigDict(extra='forbid')
    
    login: str = Field(..., description='Логин пользователя')
    roles: List[UserRole] = Field(..., description='Список ролей пользователя')
    medium_picture_url: str = Field(None, alias='mediumPictureUrl', description='URL средней аватарки')
    small_picture_url: str = Field(None, alias='smallPictureUrl', description='URL маленькой аватарки')
    status: str = Field(None, alias='status', description='Статус пользователя')
    rating: Rating = Field(..., description='Рейтинг пользователя')
    online: datetime = Field(..., description='Время последнего входа')
    name: str = Field(None, alias='name', description='Имя пользователя')
    location: str = Field(None, alias='location', description='Местоположение пользователя')
    registration: datetime = Field(..., description='Дата регистрации')
    icq: str = Field(None, alias='icq', description='ICQ номер')
    skype: str = Field(None, alias='skype', description='Skype логин')
    original_picture_url: str = Field(None, alias='originalPictureUrl', description='URL оригинальной аватарки')
    info: Any = Field(None, description='Дополнительная информация о пользователе')
    settings: UserSettings = Field(..., description='Настройки пользователя')


class UserDetailsEnvelope(BaseModel):
    """
    Обертка для детальной информации о пользователе.
    
    Стандартная структура ответа API, содержащая детальную информацию
    о пользователе и дополнительные метаданные.
    """
    model_config = ConfigDict(extra='forbid')
    
    resource: Optional[UserDetails] = Field(None, description='Детальная информация о пользователе')
    metadata: Optional[str] = Field(None, description='Дополнительные метаданные')