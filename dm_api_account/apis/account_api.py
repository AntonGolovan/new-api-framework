from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            json_data
    ):
        """
         Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=json_data
        )
        return response

    def post_v1_account_password(
            self,
            **kwargs
    ):
        """
        Reset registered user password
        :param json:
        :return:
        """
        responce = self.post(
            path=f'/v1/account/password',
            **kwargs
        )
        return responce

    def put_v1_account_password(
            self,
            **kwargs
    ):
        """
        Change registered user password
        :param:
        :return:
        """
        responce = self.put(
            path=f'/v1/account/password',
            **kwargs
        )
        return responce


    def get_v1_account(
            self,
            **kwargs
    ):
        """
        Get current user
        :param kwargs:
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
         Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        return response

    def put_v1_account_email(
            self,
            json_data
    ):
        """
         Reset registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path=f'/v1/account/email',
            json=json_data
        )
        return response

    def delete_v1_account_login(
            self,
            **kwargs
    ):
        """
        Logout as current user
        :return:
        """
        self.delete(
            path=f'/v1/account/login',
            **kwargs
        )


    def delete_v1_account_login_all(
            self,
            **kwargs
    ):
        """
        Logout from every device
        :return:
        """
        self.delete(
            path=f'/v1/account/login/all',
            **kwargs
        )