from typing import Union, Any, Dict
from requests import Response
from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient
from dm_api_account.models.registration import Registration

class AccountApi(RestClient):
    """
    API-клиент для работы с аккаунтами пользователей.
    
    Предоставляет методы для регистрации, аутентификации, управления профилем
    и другими операциями с аккаунтами пользователей.
    """

    def post_v1_account(self, registration: Registration) -> Response:
        """
        Регистрация нового пользователя.
        
        Args:
            registration (Registration): Данные для регистрации пользователя
            
        Returns:
            requests.Response: HTTP-ответ от сервера
            
        Raises:
            requests.HTTPError: Если регистрация не удалась
        """
        response: Response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            validate_response: bool = True,
            **kwargs: Any
    ) -> Union[UserEnvelope, Response]:
        """
        Сброс пароля зарегистрированного пользователя.
        
        Args:
            reset_password (ResetPassword): Данные для сброса пароля
            validate_response (bool): Валидировать ли ответ в модель UserEnvelope
            **kwargs: Дополнительные параметры запроса
            
        Returns:
            UserEnvelope или requests.Response: Валидированный ответ или сырой HTTP-ответ
            
        Raises:
            requests.HTTPError: Если сброс пароля не удался
        """
        response: Response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            validate_response: bool = True,
            **kwargs: Any
    ) -> Union[UserEnvelope, Response]:
        """
        Изменение пароля зарегистрированного пользователя.
        
        Args:
            change_password (ChangePassword): Данные для изменения пароля
            validate_response (bool): Валидировать ли ответ в модель UserEnvelope
            **kwargs: Дополнительные параметры запроса
            
        Returns:
            UserEnvelope или requests.Response: Валидированный ответ или сырой HTTP-ответ
            
        Raises:
            requests.HTTPError: Если изменение пароля не удалось
        """
        response: Response = self.put(
            path=f'/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def get_v1_account(
            self,
            validate_response: bool = True,
            **kwargs: Any
    ) -> Union[UserDetailsEnvelope, Response]:
        """
        Получение данных текущего пользователя.
        
        Args:
            validate_response (bool): Валидировать ли ответ в модель UserDetailsEnvelope
            **kwargs: Дополнительные параметры запроса
            
        Returns:
            UserDetailsEnvelope или requests.Response: Валидированный ответ или сырой HTTP-ответ
            
        Raises:
            requests.HTTPError: Если получение данных не удалось
        """
        response: Response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        if validate_response:
           return UserDetailsEnvelope(**response.json())
        return response

    def put_v1_account_token(
            self,
            token: str,
            validate_response: bool = True
    ) -> Union[UserEnvelope, Response]:
        """
        Активация зарегистрированного пользователя по токену.
        
        Args:
            token (str): Токен активации
            validate_response (bool): Валидировать ли ответ в модель UserEnvelope
            
        Returns:
            UserEnvelope или requests.Response: Валидированный ответ или сырой HTTP-ответ
            
        Raises:
            requests.HTTPError: Если активация не удалась
        """
        headers: Dict[str, str] = {'accept': 'text/plain',}
        response: Response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        if validate_response:
           return UserEnvelope(**response.json())
        return response

    def put_v1_account_email(
            self,
            change_email: ChangeEmail
    ) -> Response:
        """
        Изменение email зарегистрированного пользователя.
        
        Args:
            change_email (ChangeEmail): Данные для изменения email
            
        Returns:
            requests.Response: HTTP-ответ от сервера
            
        Raises:
            requests.HTTPError: Если изменение email не удалось
        """
        response: Response = self.put(
            path=f'/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def delete_v1_account_login(
            self,
            **kwargs: Any
    ) -> None:
        """
        Выход текущего пользователя из системы.
        
        Args:
            **kwargs: Дополнительные параметры запроса
            
        Raises:
            requests.HTTPError: Если выход не удался
        """
        self.delete(
            path=f'/v1/account/login',
            **kwargs
        )

    def delete_v1_account_login_all(
            self,
            **kwargs: Any
    ) -> None:
        """
        Выход пользователя со всех устройств.
        
        Args:
            **kwargs: Дополнительные параметры запроса
            
        Raises:
            requests.HTTPError: Если выход не удался
        """
        self.delete(
            path=f'/v1/account/login/all',
            **kwargs
        )