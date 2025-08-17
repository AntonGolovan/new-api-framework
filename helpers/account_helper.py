import time
from json import loads
from requests import JSONDecodeError, Response
from typing import Optional, Union, Any
from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_envelope import UserEnvelope
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from retrying import retry


def retry_if_result_none(result: Any) -> bool:
    """
    Функция для определения необходимости повторной попытки.
    
    Args:
        result: Результат выполнения операции
        
    Returns:
        bool: True если результат None (нужна повторная попытка), False в противном случае
    """
    return result is None


class AccountHelper:
    """
    Вспомогательный класс для работы с аккаунтами пользователей.
    
    Предоставляет высокоуровневые методы для регистрации, аутентификации,
    управления профилем и работы с email-активацией.
    """

    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ) -> None:
        """
        Инициализация AccountHelper.
        
        Args:
            dm_account_api (DMApiAccount): Клиент API аккаунтов
            mailhog (MailHogApi): Клиент MailHog для работы с email
        """
        self.dm_account_api: DMApiAccount = dm_account_api
        self.mailhog: MailHogApi = mailhog

    def auth_client(
            self,
            login: str,
            password: str
    ) -> None:
        """
        Аутентификация клиента и установка токена для последующих запросов.
        
        Args:
            login (str): Логин пользователя
            password (str): Пароль пользователя
            
        Raises:
            requests.HTTPError: Если аутентификация не удалась
        """
        response: Union[UserEnvelope, Response] = self.user_login(login=login, password=password)
        auth_token: dict = {
            'x-dm-auth-token': response.headers['x-dm-auth-token']
        }
        self.dm_account_api.account_api.set_headers(auth_token)
        self.dm_account_api.login_api.set_headers(auth_token)

    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ) -> str:
        """
        Изменение пароля пользователя с автоматическим получением токена активации.
        
        Args:
            login (str): Логин пользователя
            email (str): Email пользователя
            old_password (str): Старый пароль
            new_password (str): Новый пароль
            
        Returns:
            str: Новый пароль
            
        Raises:
            requests.HTTPError: Если изменение пароля не удалось
        """
        self.reset_user_password(login=login, email=email)
        token: str = self.fetch_activation_token(login=login)

        change_password: ChangePassword = ChangePassword(
            login=login,
            token=token,
            oldPassword=old_password,
            newPassword=new_password
        )
        self.dm_account_api.account_api.put_v1_account_password(change_password)
        return new_password

    def reset_user_password(
            self,
            login: str,
            email: str
    ) -> None:
        """
        Сброс пароля пользователя.
        
        Args:
            login (str): Логин пользователя
            email (str): Email пользователя
            
        Raises:
            requests.HTTPError: Если сброс пароля не удался
        """
        reset_password: ResetPassword = ResetPassword(
            login=login,
            email=email
        )
        self.dm_account_api.account_api.post_v1_account_password(reset_password)

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ) -> Response:
        """
        Регистрация нового пользователя с автоматической активацией.
        
        Args:
            login (str): Логин пользователя
            password (str): Пароль пользователя
            email (str): Email пользователя
            
        Returns:
            requests.Response: Ответ от сервера после активации
            
        Raises:
            AssertionError: Если регистрация или активация не удались
            requests.HTTPError: Если запрос к API не удался
        """
        registration: Registration = Registration(
            login=login,
            password=password,
            email=email
        )
        response: Response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f'Пользователь не создан {response.json()}'
        start_time: float = time.time()
        token: Optional[str] = self.get_activation_token_by_login(login=login)
        end_time: float = time.time()
        assert end_time - start_time < 3, "Время ожидания активации превышено"
        assert token is not None, f'Токен для пользователя {login} не был получен'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token, validate_response=False)
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response: bool = False,
            validate_headers: bool = False
    ) -> Union[UserEnvelope, Response]:
        """
        Вход пользователя в систему.
        
        Args:
            login (str): Логин пользователя
            password (str): Пароль пользователя
            remember_me (bool, optional): Флаг "Запомнить меня". По умолчанию True
            validate_response (bool, optional): Валидировать ли ответ. По умолчанию False
            validate_headers (bool, optional): Проверять ли наличие токена в заголовках. По умолчанию False
            
        Returns:
            UserEnvelope или requests.Response: Ответ от сервера
            
        Raises:
            requests.HTTPError: Если вход не удался
            AssertionError: Если validate_headers=True и токен отсутствует
        """
        login_credentials: LoginCredentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )
        response: Union[UserEnvelope, Response] = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        if validate_headers:
            assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"
        return response

    def user_logout(self) -> None:
        """
        Выход текущего пользователя из системы.
        
        Raises:
            requests.HTTPError: Если выход не удался
        """
        self.dm_account_api.account_api.delete_v1_account_login()

    def user_logout_every_device(self) -> None:
        """
        Выход пользователя со всех устройств.
        
        Raises:
            requests.HTTPError: Если выход не удался
        """
        self.dm_account_api.account_api.delete_v1_account_login_all()

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self, login: str) -> Optional[str]:
        """
        Получение токена активации для пользователя по логину.
        
        Метод выполняет повторные попытки до 5 раз с интервалом 1 секунда,
        если токен не найден.
        
        Args:
            login (str): Логин пользователя
            
        Returns:
            str или None: Токен активации или None если не найден
        """
        token: Optional[str] = None
        response: Response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            try:
                user_data: dict = loads(item['Content']['Body'])
            except (JSONDecodeError, KeyError):
                print("Ошибка декодирования JSON")
            user_login: str = user_data['Login']
            if user_login == login and user_data.get('ConfirmationLinkUrl'):
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            else:
                token = user_data['ConfirmationLinkUri'].split('/')[-1]
            return token

    def change_email_user(
            self,
            login: str,
            password: str,
            email: str
    ) -> Response:
        """
        Изменение email пользователя.
        
        Args:
            login (str): Логин пользователя
            password (str): Пароль пользователя
            email (str): Новый email
            
        Returns:
            requests.Response: Ответ от сервера
            
        Raises:
            requests.HTTPError: Если изменение email не удалось
            AssertionError: Если статус ответа не 200
        """
        change_email: ChangeEmail = ChangeEmail(
            login=login,
            password=password,
            email=email
        )
        response: Response = self.dm_account_api.account_api.put_v1_account_email(change_email)
        assert response.status_code == 200, f'Не успешная попытка изменить email {response.json()}'
        return response

    def fetch_activation_token(
            self,
            login: str
    ) -> str:
        """
        Получение токена активации с проверкой его наличия.
        
        Args:
            login (str): Логин пользователя
            
        Returns:
            str: Токен активации
            
        Raises:
            AssertionError: Если токен не найден
        """
        token: Optional[str] = self.get_activation_token_by_login(login=login)
        assert token is not None, f'Токен для пользователя {login} не был получен'
        return token

    def activate_user(
            self,
            token: str,
            validate_response: bool
    ) -> Response:
        """
        Активация пользователя по токену.
        
        Args:
            token (str): Токен активации
            validate_response (bool): Валидировать ли ответ
            
        Returns:
            requests.Response: Ответ от сервера
            
        Raises:
            requests.HTTPError: Если активация не удалась
            AssertionError: Если статус ответа не 200
        """
        response: Response = self.dm_account_api.account_api.put_v1_account_token(
            token=token, validate_response=validate_response
            )
        assert response.status_code == 200, 'Пользователь не был активирован'