from checkers.http_checkers import check_status_code_http

def test_put_v1_account_email(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_email_user(login=login, password=password, email=f'ant{email}')
    with check_status_code_http(
            expected_status_code=403,
            expected_message='User is inactive. Address the technical support for more details'
    ):
        account_helper.user_login(login=login, password=password)
    token = account_helper.fetch_activation_token(login=login)
    account_helper.activate_user(token=token, validate_response=False)
    account_helper.user_login(login=login, password=password)