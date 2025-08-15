from json import (loads,JSONDecodeError)
import time

from api_account.apis.account_api import AccountApi
from api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
import structlog

from tests.functional.post_v1_account.test_post_v1_account import get_activation_token_by_login

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)

def test_put_v1_account_email():

    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')

    account_api= AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    # Регистрация пользователя

    login = 'ag5'
    password = '112233'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)

    print(response.status_code)
    print(response.text)

    assert response.status_code == 201, f'Пользователь не создан {response.json()}'

    # Получить письмо из почтового сервиса

    response = mailhog_api.get_api_v2_messages()

    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, 'Письма не были получены'
    time.sleep(1)

    # Получить токен активации из письма

    token = get_activation_token_by_login(login=login, response=response)

    assert token is not None, f'Токен для пользователя {login} не был получен'

    # Активация пользователя

    response = account_api.put_v1_account_token(token=token)

    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, f'Пользователь не авторизован'

    # Авторизация пользователя

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, f'Пользователь не был активирован'

    # Изменяем адрес почты пользователя

    json_data = {
        'login': login,
        'password': password,
        'email': f'ant{email}'
    }

    response = account_api.put_v1_account_email(json_data=json_data)

    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, f'Не успешная попытка изменить email {response.json()}'

    # Авторизация пользователя после смены адреса почты

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)

    assert response.status_code == 403, f'Пользователь не авторизован {response.json()}'

    # Получить письмо из почтового сервиса

    response = mailhog_api.get_api_v2_messages()

    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, 'Письма не были получены'
    time.sleep(1)

    # Получаем новый токен активации после смены адреса почты

    token = get_activation_token_by_login(login=login, response=response)

    assert token is not None, f'Токен для пользователя {login} не был получен'

    # Авторизация пользователя

    response = account_api.put_v1_account_token(token=token)

    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, f'Пользователь не авторизован'

# Активация пользователя новым токеном

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, f'Пользователь не был активирован'