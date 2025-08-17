from typing import Optional
import requests
from restclient.client import RestClient


class MailhogApi(RestClient):
    """
    API-клиент для работы с MailHog.
    
    Предоставляет методы для получения email-сообщений из тестового почтового сервера
    MailHog, который используется для тестирования email-функциональности.
    """

    def get_api_v2_messages(
            self,
            limit: int = 50
    ) -> requests.Response:
        """
        Получение email-сообщений из MailHog.
        
        Args:
            limit (int, optional): Максимальное количество сообщений для получения. По умолчанию 50
            
        Returns:
            requests.Response: HTTP-ответ с email-сообщениями
            
        Raises:
            requests.HTTPError: Если получение сообщений не удалось
        """
        params: dict = {
            'limit': limit
        }

        response: requests.Response = self.get(
            path=f'/api/v2/messages',
            params=params,
            verify=False
        )
        return response