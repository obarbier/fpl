""" Package that Handles all API Request to FPL"""
# Os import sections

# third party import
from fpl import FPL
from fplsupercharge.Utils.protosUtils import parse_dict
from fplsupercharge.protos.apiServices_pb2 import Teams
# local import


class FplRequestApiHandler(FPL):
    async def get_proto_team(self) -> Teams:
        res = Teams()
        teams = await self.get_teams(return_json=True)
        for t in teams:
            team = res.team.add()
            team = parse_dict(t, team)
        return res

    async def get_mini_league_stats(self, id: int):
        pass
