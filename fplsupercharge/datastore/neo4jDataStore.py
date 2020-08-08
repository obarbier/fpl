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
        query = """
        UNWIND $team AS properties
        CREATE (n:Team)
        SET n = properties
        """
        with self.driver.session() as session:
            session.run(query, team=list_teams)

    def create_players(self, list_players):
        query = """
        UNWIND $player AS properties
        CREATE (n:Player)
        SET n = properties
        """
        with self.driver.session() as session:
            session.run(query, player=list_players)

    def player_playsIn_team(self):
        with self.driver.session() as session:
            session.run(
                "MATCH (a:Player),(b:Team) WHERE a.team = b.id create (a)-[r:playsIn]->(b)")

    def create_league(self, list_leagues):
        query = """
        UNWIND $league AS properties
        CREATE (n:League)
        SET n = properties
        """
        with self.driver.session() as session:
            session.run(query, league=list_leagues)

    def create_user(self, list_users):
        query = """
        UNWIND $user AS properties
        CREATE (n:User)
        SET n = properties
        """
        with self.driver.session() as session:
            session.run(query, user=list_users)

    def create_user_and_leagues(self, user, list_leagues):
        query = """
        CREATE (u:User ) set u = $user
        WITH u
        UNWIND $leagues AS league
        CREATE (u)-[:IN]->(l:League) set l = league
        """
        with self.driver.session() as session:
            session.run(query, user=user, leagues=list_leagues)

    def map_user_picks(self, user_id, gameweek_id, gameweek_picks):
        # gameweek_picks = map(json.dumps,gameweek_picks)
        query = """
        UNWIND $gameweek_picks as pick
        MATCH (p:Player) , (u:User) WHERE u.id = $user_id and
        p.id = pick.element
        MERGE (u)-[rel:OWN]->(p) set rel = pick, 
        rel.gameweek_id =  COALESCE(rel.gameweek_id , []) + $gameweek_id 
        """
        with self.driver.session() as session:
            session.run(query, user_id=user_id,
                        gameweek_id=gameweek_id, gameweek_picks=gameweek_picks)
