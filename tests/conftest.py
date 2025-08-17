import pytest
import structlog
from faker import Faker
from datetime import datetime
from collections import namedtuple
from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

# Настройка структурированного логирования
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)


@pytest.fixture(scope="session")
def mailhog_api():
    """
    Фикстура для создания клиента MailHog API.
    
    Создает клиент для работы с тестовым почтовым сервером MailHog.
    Область действия - сессия (создается один раз на всю тестовую сессию).
    
    Returns:
        MailHogApi: Клиент MailHog API
    """
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope="session")
def account_api():
    """
    Фикстура для создания клиента API аккаунтов.
    
    Создает клиент для работы с API управления аккаунтами пользователей.
    Область действия - сессия (создается один раз на всю тестовую сессию).
    
    Returns:
        DMApiAccount: Клиент API аккаунтов
    """
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope="function")
def auth_account_helper(mailhog_api):
    """
    Фикстура для создания предварительно аутентифицированного AccountHelper.
    
    Создает AccountHelper с уже выполненной аутентификацией пользователя.
    Область действия - функция (создается для каждого теста).
    
    Args:
        mailhog_api: Клиент MailHog API (внедряется автоматически)
        
    Returns:
        AccountHelper: Предварительно аутентифицированный helper
    """
    dm_api_configuration = DmApiConfiguration(
        host='http://5.63.153.31:5051', disable_log=False
    )
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(
        login="golovan010",
        password="112233"
    )
    return account_helper


@pytest.fixture(scope="session")
def account_helper(
        account_api,
        mailhog_api
):
    """
    Фикстура для создания AccountHelper.
    
    Создает AccountHelper для работы с аккаунтами пользователей.
    Область действия - сессия (создается один раз на всю тестовую сессию).
    
    Args:
        account_api: Клиент API аккаунтов (внедряется автоматически)
        mailhog_api: Клиент MailHog API (внедряется автоматически)
        
    Returns:
        AccountHelper: Helper для работы с аккаунтами
    """
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture
def prepare_user():
    """
    Фикстура для создания уникального тестового пользователя.
    
    Генерирует уникальные данные пользователя с временной меткой,
    что позволяет избежать конфликтов при параллельном выполнении тестов.
    Область действия - функция (создается для каждого теста).
    
    Returns:
        namedtuple: Объект с полями login, password, email
    """
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
    login = f'golovan_{data}'
    password = '112233'
    email = f'{login}@mail.ru'
    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user


@pytest.fixture(name="fake")
def fake_data():
    """
    Фикстура для генерации тестовых данных.
    
    Создает экземпляр Faker для генерации реалистичных тестовых данных
    (имена, email, пароли и т.д.).
    
    Returns:
        Faker: Генератор тестовых данных
    """
    fake = Faker()
    return fake
