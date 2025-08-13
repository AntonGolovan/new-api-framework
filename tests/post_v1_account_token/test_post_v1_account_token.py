import requests


def test_post_v1_account():
    ### Регистрация пользователя

    login = "golovan_2"
    email = f"{login}@mail.ru"
    password = "123456"

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    ### Поулчить письма из почтового сервиса

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    ### Получить активационный токен

    ...

    ### Активация пользователя

    response = requests.put('http://5.63.153.31:5051/v1/account/642ecd73-1c5b-4958-9b9c-ef4cb4c83845')
    ### Авторизоваться

    json_data = {
        'login': login,
        'password': login,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    ...
