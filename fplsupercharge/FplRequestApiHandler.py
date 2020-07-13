""" Package that Handles all API Request to FPL"""
# Os import sections

# third party import
from uplink import Consumer, get

# local import
from fplsupercharge.Utils.constants import API_URLS
from fplsupercharge.protos.team_pb2 import Teams


class FplRequestApiHandler(Consumer):
    @get(API_URLS["static"])
    def get_teams(self) -> Teams:
        """get static response"""
