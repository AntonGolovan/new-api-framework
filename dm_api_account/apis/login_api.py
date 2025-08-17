from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient

class LoginApi(RestClient):
    """
    API-клиент для аутентификации пользователей.
    
    Предоставляет методы для входа пользователей в систему с использованием
    учетных данных (логин/пароль).
    """

    def post_v1_account_login(
            self,
            login_credentials: LoginCredentials,
            validate_response=True
    ):
        """
        Аутентификация пользователя по учетным данным.
        
        Args:
            login_credentials (LoginCredentials): Данные для входа (логин, пароль, remember_me)
            validate_response (bool): Валидировать ли ответ в модель UserEnvelope
            
        Returns:
            UserEnvelope или requests.Response: Валидированный ответ или сырой HTTP-ответ
            
        Raises:
            requests.HTTPError: Если аутентификация не удалась
        """
        response = self.post(
            path=f'/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
           return UserEnvelope(**response.json())
        return response