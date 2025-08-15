from restclient.configuration import Configuration
from api_account.apis.account_api import AccountApi
from api_account.apis.login_api import LoginApi


class DMApiAccount:

    def __init__(
            self,
            configuration: Configuration
    ):
        self.configuration = configuration
        self.account_api = AccountApi(configuration=configuration)
        self.login_api = LoginApi(configuration=configuration)