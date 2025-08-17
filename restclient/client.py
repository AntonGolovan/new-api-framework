
from requests import (session, JSONDecodeError, Response, Session)
import structlog
import uuid
import curlify
from typing import Optional, Dict, Any

from restclient.configuration import Configuration


class RestClient:
    """
    Базовый HTTP-клиент для работы с REST API.
    
    Предоставляет методы для выполнения HTTP-запросов с автоматическим логированием,
    генерацией cURL-команд и обработкой ошибок.
    """

    def __init__(
            self,
            configuration: Configuration
    ) -> None:
        """
        Инициализация HTTP-клиента.
        
        Args:
            configuration (Configuration): Конфигурация клиента, содержащая host, headers и настройки логирования
        """
        self.host: str = configuration.host
        self.set_headers(configuration.headers)
        self.disable_log: bool = configuration.disable_log
        self.session: Session = session()
        self.log = structlog.getLogger(__name__).bind(service='api')

    def set_headers(self, headers: Optional[Dict[str, str]]) -> None:
        """
        Установка HTTP-заголовков для всех запросов.
        
        Args:
            headers (dict): Словарь с заголовками для установки
        """
        if headers:
            self.session.headers.update(headers)

    def post(
            self,
            path: str,
            **kwargs: Any
    ) -> Response:
        """
        Выполнение HTTP POST запроса.
        
        Args:
            path (str): Путь запроса (будет добавлен к базовому URL)
            **kwargs: Дополнительные параметры запроса (json, data, headers, params и т.д.)
            
        Returns:
            requests.Response: Ответ от сервера
            
        Raises:
            requests.HTTPError: Если сервер вернул ошибку HTTP
        """
        return self._send_request(method='POST', path=path, **kwargs)

    def get(
            self,
            path: str,
            **kwargs: Any
    ) -> Response:
        """
        Выполнение HTTP GET запроса.
        
        Args:
            path (str): Путь запроса (будет добавлен к базовому URL)
            **kwargs: Дополнительные параметры запроса (params, headers и т.д.)
            
        Returns:
            requests.Response: Ответ от сервера
            
        Raises:
            requests.HTTPError: Если сервер вернул ошибку HTTP
        """
        return self._send_request(method='GET', path=path, **kwargs)

    def put(
            self,
            path: str,
            **kwargs: Any
    ) -> Response:
        """
        Выполнение HTTP PUT запроса.
        
        Args:
            path (str): Путь запроса (будет добавлен к базовому URL)
            **kwargs: Дополнительные параметры запроса (json, data, headers, params и т.д.)
            
        Returns:
            requests.Response: Ответ от сервера
            
        Raises:
            requests.HTTPError: Если сервер вернул ошибку HTTP
        """
        return self._send_request(method='PUT', path=path, **kwargs)

    def delete(
            self,
            path: str,
            **kwargs: Any
    ) -> Response:
        """
        Выполнение HTTP DELETE запроса.
        
        Args:
            path (str): Путь запроса (будет добавлен к базовому URL)
            **kwargs: Дополнительные параметры запроса (headers, params и т.д.)
            
        Returns:
            requests.Response: Ответ от сервера
            
        Raises:
            requests.HTTPError: Если сервер вернул ошибку HTTP
        """
        return self._send_request(method='DELETE', path=path, **kwargs)

    def _send_request(self, method: str, path: str, **kwargs: Any) -> Response:
        """
        Внутренний метод для выполнения HTTP-запросов.
        
        Выполняет запрос с логированием, генерацией cURL-команд и обработкой ошибок.
        
        Args:
            method (str): HTTP-метод (GET, POST, PUT, DELETE)
            path (str): Путь запроса
            **kwargs: Параметры запроса
            
        Returns:
            requests.Response: Ответ от сервера
            
        Raises:
            requests.HTTPError: Если сервер вернул ошибку HTTP
        """
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url: str = self.host + path

        if self.disable_log:
            rest_response: Response = self.session.request(method=method, url=full_url, **kwargs)
            rest_response.raise_for_status()  # Метод выбрасывает исключение если ответ от сервера отличается от 200
            return rest_response

        log.msg(
            event='Request',
            method=method,
            full_url=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get('headers'),
            json=kwargs.get('json'),
            data=kwargs.get('data'),
        )
        rest_response: Response = self.session.request(method=method, url=full_url, **kwargs)

        curl: str = curlify.to_curl(rest_response.request)
        print(curl)

        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            json=self._get_json(rest_response)
        )
        rest_response.raise_for_status()  # Метод выбрасывает исключение если ответ от сервера отличается от 200
        return rest_response

    @staticmethod
    def _get_json(rest_response: Response) -> Dict[str, Any]:
        """
        Извлечение JSON из HTTP-ответа.
        
        Args:
            rest_response (requests.Response): HTTP-ответ
            
        Returns:
            dict: JSON-данные или пустой словарь в случае ошибки парсинга
        """
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}