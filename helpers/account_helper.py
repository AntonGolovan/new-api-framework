import time
from json import loads
from requests import JSONDecodeError
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
        auth_token = {'x-dm-auth-token': response.headers['x-dm-auth-token']}
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
        self.dm_account_api.account_api.put_v1_account_password(
            json={
                'login': login,
                'token': token,
                'oldPassword': old_password,
                'newPassword': new_password,
            }
        )
        self.user_login(login=login, password=new_password)

    def reset_user_password(
            self,
            login: str,
            email: str
    ):
        self.dm_account_api.account_api.post_v1_account_password(
            json={
                'login': login,
                'email': email
            }
        )

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не создан {response.json()}'

        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f'Токен для пользователя {login} не был получен'

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Пользователь не был активирован'

        return response


    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, 'Пользователь не был авторизован'
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
        json_data = {
            'login': login,
            'password': password,
            'email': f'ant.{email}',
        }

        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, f'Не успешная попытка изменить email {response.json()}'
        return response


    def fetch_activation_token(self,login):
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f'Токен для пользователя {login} не был получен'
        return token


    def activate_user(self,token):
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Пользователь не был активирован'