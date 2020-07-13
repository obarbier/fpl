""" Package that test all API Request to FPL"""
# Os import
import unittest

# third party import

# local import
from fplsupercharge.Utils.constants import API_BASE_URL
from fplsupercharge.protos.team_pb2 import Teams
from fplsupercharge.converter.ProtobuffConverter import ProtobuffConverter
from fplsupercharge.FplRequestApiHandler import FplRequestApiHandler


class test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(test, self).__init__(*args, **kwargs)
        self.fplRequestApiHandler = FplRequestApiHandler(
            base_url=API_BASE_URL, converter=ProtobuffConverter())

    def test_static(self):
        response = self.fplRequestApiHandler.get_teams()
        self.assertTrue(isinstance(response, Teams))


if __name__ == '__main__':
    unittest.main()
