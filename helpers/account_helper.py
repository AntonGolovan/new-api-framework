import time
from json import loads
from requests import JSONDecodeError
from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from retrying import retry


def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


class AccountHelper:

    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.user_login(login=login, password=password)
        auth_token = {
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
    ):
        self.reset_user_password(login=login, email=email)
        token = self.fetch_activation_token(login=login)

        change_password = ChangePassword(
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
    ):
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        self.dm_account_api.account_api.post_v1_account_password(reset_password)

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login=login,
            password=password,
            email=email
        )
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f'Пользователь не создан {response.json()}'
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активации превышено"
        assert token is not None, f'Токен для пользователя {login} не был получен'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token, validate_response=False)
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response=False,
            validate_headers=False
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        if validate_headers:
            assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"
        return response

    def user_logout(self):
        self.dm_account_api.account_api.delete_v1_account_login()

    def user_logout_every_device(self):
        self.dm_account_api.account_api.delete_v1_account_login_all()

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self,login):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            try:
                user_data = loads(item['Content']['Body'])
            except (JSONDecodeError, KeyError):
                print("Ошибка декодирования JSON")
            user_login = user_data['Login']
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
    ):
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=email
        )
        response = self.dm_account_api.account_api.put_v1_account_email(change_email)
        assert response.status_code == 200, f'Не успешная попытка изменить email {response.json()}'
        return response

    def fetch_activation_token(
            self,
            login
    ):
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f'Токен для пользователя {login} не был получен'
        return token

    def activate_user(
            self,
            token,
            validate_response
    ):
        response = self.dm_account_api.account_api.put_v1_account_token(
            token=token, validate_response=validate_response
            )
        assert response.status_code == 200, 'Пользователь не был активирован'