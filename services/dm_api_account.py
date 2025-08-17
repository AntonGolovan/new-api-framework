from restclient.configuration import Configuration
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi


class DMApiAccount:
    """
    Сервисный класс для работы с API аккаунтов.
    
    Объединяет AccountApi и LoginApi в единый интерфейс для работы
    с аккаунтами пользователей.
    """

    def __init__(
            self,
            configuration: Configuration
    ) -> None:
        """
        Инициализация сервиса API аккаунтов.
        
        Args:
            configuration (Configuration): Конфигурация для подключения к API
        """
        self.configuration: Configuration = configuration
        self.account_api: AccountApi = AccountApi(configuration=configuration)
        self.login_api: LoginApi = LoginApi(configuration=configuration)