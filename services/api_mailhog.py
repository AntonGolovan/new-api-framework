from restclient.configuration import Configuration
from api_mailhog.apis.mailhog_api import MailhogApi


class MailHogApi:
    """
    Сервисный класс для работы с MailHog API.
    
    Предоставляет удобный интерфейс для работы с тестовым почтовым сервером
    MailHog, используемым для тестирования email-функциональности.
    """

    def __init__(
            self,
            configuration: Configuration
    ) -> None:
        """
        Инициализация сервиса MailHog.
        
        Args:
            configuration (Configuration): Конфигурация для подключения к MailHog
        """
        self.configuration: Configuration = configuration
        self.mailhog_api: MailhogApi = MailhogApi(configuration=configuration)