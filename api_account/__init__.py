"""
Модуль API для управления пользовательскими аккаунтами.

Этот модуль содержит классы для работы с основными функциями
управления пользователями, включая регистрацию, активацию и авторизацию.

Модули:
    apis.account_api: Операции с аккаунтами (регистрация, активация, смена email)
    apis.login_api: Операции авторизации пользователей

Пример использования:
    from api_account.apis.account_api import AccountApi
    from api_account.apis.login_api import LoginApi
    
    # Создание API клиентов
    account_api = AccountApi(host='http://example.com:5051')
    login_api = LoginApi(host='http://example.com:5051')
"""

