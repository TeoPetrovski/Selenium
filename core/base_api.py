import sys

import requests

from core.constants import Environment


class BaseApi:
    """Contains logic that can be used in all requests such as base api, request headers, tokens..."""

    def __init__(self, environment: str):
        self.environment = environment

    def get_base_api(self):
        if self.environment in Environment.API_URLS.keys():
            return Environment.API_URLS[self.environment]
        else:
            sys.exit("Environment not defined!")

    def get_page_response(self, endpoint: str):
        """Gets response for the specified webpage endpoint.

        Params:
            endpoint: webpage endpoint
        """
        url = f"{self.get_base_api()}{endpoint}"
        return requests.get(url)
