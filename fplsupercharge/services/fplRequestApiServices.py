""" Package that Handles all API Request to FPL"""
# Os import sections

# third party import
import fpl
from fplsupercharge.utils.protosUtils import parse_dict
from fplsupercharge.protos.apiServices_pb2 import Teams
# local import


fpl.utils.headers = {"User-Agent": "PostmanRuntime/7.26.1"}


class FplRequestApiHandler(fpl.FPL):
    async def get_proto_team(self) -> Teams:
        res = Teams()
        teams = await self.get_teams(return_json=True)
        for t in teams:
            team = res.team.add()
            team = parse_dict(t, team)
        return res

    async def get_user_picks(self, id: int = None, gameweek=None):
        json_user = await self.get_user(user_id=id)
        picks = await json_user.get_picks(gameweek=None)
        return picks

    async def get_user_classic_leagues(self, id: int = None, return_json=False):
        json_user = await self.get_user(user_id=id, return_json=True)
        json_leagues = json_user['leagues']['classic']
        classic_leagues = [await self.get_classic_league(
            league['id'], return_json=return_json) for league in json_leagues]
        return classic_leagues

    async def get_mini_league_stats(self, id: int):
        # TODO: a way to get static about minileagues
        # this could be implemented in database
        pass

    async def generate_dream_team_info(self, id):
        # TODO: Need to create a speacial User called (dreamTeam) and track
        # progress over the seasson
        pass