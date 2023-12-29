import requests

from src.qawa.core.constants import Environment


class BaseApi:
    """Contains logic that can be used in all requests such as base api, request headers, tokens..."""

    def __init__(self, environment: Environment):
        self.environment = environment

    def get_page_response(self, endpoint: str):
        """Gets response for the specified webpage endpoint.

        Params:
            endpoint: webpage endpoint
        """

        url = f"{self.environment.api_url}{endpoint}"
        return requests.get(url)
