import requests

from src.qawa.core.constants import EnvironmentApiUrl, Environment


class BaseApi:
    """Contains logic that can be used in all requests such as base api, request headers, tokens..."""

    def __init__(self, environment: str):
        self.environment = environment

    def get_base_api_url(self):
        """Gets base API URL for the initialized environment."""
        if self.environment == Environment.PROD.value:
            url = EnvironmentApiUrl.PROD.value
        else:
            url = EnvironmentApiUrl.DEV.value

        return url

    def get_page_response(self, endpoint: str):
        """Gets response for the specified webpage endpoint.

        Params:
            endpoint: webpage endpoint
        """
        url = f"{self.get_base_api_url()}{endpoint}"
        return requests.get(url)
