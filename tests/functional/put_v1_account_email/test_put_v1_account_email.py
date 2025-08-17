def test_put_v1_account_email(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email


    account_helper.register_new_user(login=login, password=password, email=email)

    account_helper.user_login(login=login, password=password)

    account_helper.change_email_user(login=login, password=password, email=email)

    json_data = {
        "login": login,
        "rememberMe": True,
        "password": password
    }
    response = account_helper.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, f'Пользователь не авторизован {response.json()}'

    token = account_helper.fetch_activation_token(login=login)

    account_helper.activate_user(token=token)

    account_helper.user_login(login=login, password=password)