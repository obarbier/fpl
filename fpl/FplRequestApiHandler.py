#function import
import unittest
import  inspect

#third party import
from uplink import Consumer, get, Path, Query, response_handler,returns, types

#local import
from fpl.Utils.constants import  API_BASE_URL, API_URLS
from fpl.protos.team_pb2 import Teams
from fpl.converter.ProtobuffConverter import ProtobuffConverter

class FplRequestApiHandler(Consumer):
    @get(API_URLS["static"])
    def get_teams(self) -> Teams:
        """get static response"""

class test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(test, self).__init__(*args, **kwargs)
        self.fplRequestApiHandler = FplRequestApiHandler(base_url= API_BASE_URL)
    def test_static(self):
        response= self.fplRequestApiHandler.get_teams();
        self.assertEqual(response.status_code ,200)
        self.assertTrue(response)

if __name__ == '__main__':
    unittest.main()
    
