import unittest
from requests.exceptions import HTTPError
from Utils import constants
from protos.team_pb2 import team
from uplink import Consumer, get, Path, Query, response_handler,returns

def raise_for_status(response):
    """Checks whether or not the response was successful."""
    if 200 <= response.status_code < 300:
        # Pass through the response.
        return response
    raise UnsuccessfulRequest(response.url)

class FplRequestApiHandler(Consumer):

    @get(constants.API_URLS["static"])
    @returns.json(key="teams")
    @response_handler(raise_for_status)
    def get_static(self):
        """get static response"""

class test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(test, self).__init__(*args, **kwargs)
        self.fplRequestApiHandler = FplRequestApiHandler(base_url= constants.API_BASE_URL)
    def test_static(self):
        self.assertEqual(self.fplRequestApiHandler.get_static().status_code , 200)


if __name__ == '__main__':
    unittest.main()
    
