import requests
from contextlib import contextmanager
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(
        expected_status_code: requests.codes.OK,
        expected_message: str = ""):
    """
    Контекстный менеджер для проверки HTTP-статус-кодов и сообщений об ошибках.
    
    Используется для тестирования API-ответов. Проверяет, что запрос завершился
    с ожидаемым статус-кодом и сообщением об ошибке.
    
    Args:
        expected_status_code (int): Ожидаемый HTTP-статус-код
        expected_message (str, optional): Ожидаемое сообщение об ошибке
        
    Raises:
        AssertionError: Если статус-код или сообщение не соответствуют ожидаемым
        
    Example:
        >>> with check_status_code_http(400, "Validation failed"):
        ...     api_client.post('/users', json=invalid_data)
    """
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(f"Ожидаемый статус код должен быть равен {expected_status_code}")
        if expected_message:
            raise AssertionError(f"Должно быть получено сообщение {expected_message}, но запрос прошел успешно")
    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()['title'] == expected_message