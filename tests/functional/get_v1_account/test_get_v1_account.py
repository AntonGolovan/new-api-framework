from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to, contains_inanyorder
from checkers.http_checkers import check_status_code_http


def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    assert_that(
        response, all_of(
            has_property('resource', has_property('login', starts_with('golovan'))),
            has_property(
                'resource', has_property(
                    'roles', contains_inanyorder(
                        'Guest', 'Player'
                    )
                )
            ),
            has_property(
                'resource', has_property(
                    'rating', has_properties(
                        {
                            "enabled": equal_to(True),
                            "quality": equal_to(0),
                            "quantity": equal_to(0)
                        }
                    )
                )
            )
        )
    )


def test_get_v1_account_not_auth(account_helper):
    with check_status_code_http(expected_status_code=401, expected_message="User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account()