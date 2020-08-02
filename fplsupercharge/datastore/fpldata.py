from fpl import FPL
import json
from neo4j import GraphDatabase
from logging import getLogger, StreamHandler, DEBUG
import aiohttp
import asyncio
from fplsupercharge.FplRequestApiHandler import FplRequestApiHandler
handler = StreamHandler()
handler.setLevel(DEBUG)
logger = getLogger("neo4j").addHandler(handler)


class FplDatastore:
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(
                "bolt://0.0.0.0:7687", auth=("fpl", "abcd"))
        except Exception as ex:
            print(ex)
            # logger.error("Database INITIALIZATION ERROR." + ex)

    def close(self):
        self._driver.close()

    def create_teams(self, list_teams):
        with self.driver.session() as session:
            [session.run("CREATE (n:Team) set n = $team", team=team)
             for team in list_teams]

    def create_players(self, list_players):
        with self.driver.session() as session:
            [session.run("CREATE (n:Player) set n = $player", player=player)
             for player in list_players]

    def player_playsIn_team(self):
        with self.driver.session() as session:
            session.run(
                "MATCH (a:Player),(b:Team) WHERE a.team = b.id create (a)-[r:playsIn]->(b)")

    def create_league(self, league):
        with self.driver.session() as session:
            session.run("CREATE (n:League) set n = $league", league=league)

    def create_user(self, user):
        with self.driver.session() as session:
            session.run("CREATE (n:User) set n = $user", user=user)


async def main():
    fplDatastore = FplDatastore()
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login("obarbier13@gmail.com","olivier007")
        classic_league = await fpl.get_classic_league(21)
        page = 1;
        while True:
            standing = await classic_league.get_standings(page=page)
            print(standing)
            if(standing['page']):
                page = page + 1
            else:
                break

if __name__ == "__main__":
    asyncio.run(main())
