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


class Datastore:
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

    def create_league(self, list_leagues):
        with self.driver.session() as session:
            [session.run("CREATE (n:League) set n = $league", league=league)
             for league in list_leagues]

    def create_user(self, list_users):
        with self.driver.session() as session:
            [session.run("CREATE (n:User) set n = $user", user=user)
             for user in list_users]

    def create_user_and_leagues(self, _list_users):
        pass
