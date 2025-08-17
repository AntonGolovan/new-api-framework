import random
from datetime import datetime
import pytest
from faker import Faker
from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to
from checkers.http_checkers import check_status_code_http

def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    assert_that(
        response, all_of(
            has_property('resource', has_property('login', starts_with('golovan'))),
            has_property('resource', has_property('registration', instance_of(datetime))),
            has_property(
                'resource', has_properties(
                    {
                        'rating': has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    }
                )
            )
        )
    )

fake = Faker()

@pytest.mark.parametrize(
    "login, password, email, expected_status_code, expected_message", [
        pytest.param(fake.name(), fake.password(length=5), fake.email(), 400, "Validation failed", id="Invalid password"),
        pytest.param('1', fake.password(length=random.randint(6, 8)), fake.email(), 400, "Validation failed", id='Invalid login'),
        pytest.param(fake.name(), fake.password(length=random.randint(6, 8)), "example.com", 400, "Validation failed", id='Invalid email'),
    ]
)
def test_negative_post_v1_account(account_helper, login, password, email, expected_status_code, expected_message):
    with check_status_code_http(expected_status_code=expected_status_code, expected_message=expected_message):
        account_helper.register_new_user(login=login, password=password, email=email)
