"""
Модуль API для работы с тестовым почтовым сервисом MailHog.

MailHog - это инструмент для тестирования email функциональности в процессе разработки.
Он перехватывает все исходящие письма и предоставляет веб-интерфейс и API для их просмотра.

Модули:
    apis.mailhog_api: API для получения и анализа перехваченных писем

Пример использования:
    from api_mailhog.apis.mailhog_api import MailhogApi
    
    # Создание клиента MailHog API
    mailhog_api = MailhogApi(host='http://example.com:5025')
    
    # Получение списка писем
    response = mailhog_api.get_api_v2_messages(limit=10)
"""

