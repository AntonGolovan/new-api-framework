from typing import Optional, Dict


class Configuration:
    """
    Класс конфигурации для HTTP-клиентов.
    
    Содержит настройки для подключения к API-серверам, включая базовый URL,
    заголовки и параметры логирования.
    """

    def __init__(
            self,
            host: str,
            headers: Optional[Dict[str, str]] = None,
            disable_log: bool = True
    ) -> None:
        """
        Инициализация конфигурации.
        
        Args:
            host (str): Базовый URL API-сервера (например, 'http://api.example.com')
            headers (dict, optional): Дополнительные HTTP-заголовки для всех запросов
            disable_log (bool, optional): Отключение логирования запросов. По умолчанию True
        """
        self.host: str = host
        self.headers: Optional[Dict[str, str]] = headers
        self.disable_log: bool = disable_log