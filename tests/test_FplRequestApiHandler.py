""" Package that test all API Request to FPL"""
# Os import
import unittest
import asyncio
# third party import
import aiohttp
# local import
from fplsupercharge.protos.apiServices_pb2 import Teams
from fplsupercharge.FplRequestApiHandler import FplRequestApiHandler

async def get_all_teams():
    async with aiohttp.ClientSession() as session:
        fplRequestApiHandler = FplRequestApiHandler(session)
        return await fplRequestApiHandler.get_all_teams()

class test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(test, self).__init__(*args, **kwargs)

    def test_get_all_teams(self):
        response = asyncio.run(get_all_teams())
        self.assertTrue(isinstance(response, Teams))

if __name__ == '__main__':
    unittest.main()
