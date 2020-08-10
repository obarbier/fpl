"""
This Module focus on interacting with the data The goal is to try
to make this as transperant as possible. In future realease
we should be able to deside a database and the application
will store the data as needed
"""
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from typing import Tuple


Auth = Tuple[str, str]


class Datastore:
    def __init__(self, uri, username, password, logger):
        try:
            self._logger = logger.getChild("neo4jservices")
            self._driver = GraphDatabase.driver(
                uri=uri, auth=(username, password))
            logger.info("succesfully logged into: {} ".format(uri))
        except Exception as ex:
            logger.error(
                "Driver Error occured while initializing db {}".format(ex))
            raise

    def close(self):
        self._driver.close()

    def deleteAll(self):
        query = """
        MATCH ()-[p]-(n) delete p ,n
        """
        try:
            self._logger.info("started deleteAll operation")
            with self._driver.session() as session:
                session.run(query)
            self._logger.info("successfully deleteAll operation")
        except ServiceUnavailable as exception:
            self._logger.error("{query} raised an error: \n {exception}"
                               .format(
                                   query=query, exception=exception))
            raise

    def create_teams(self, list_teams):
        self._logger.info("create_teams")
        query = """
        UNWIND $team AS properties
        CREATE (n:Team)
        SET n = properties
        """
        try:
            self._logger.info("started create_teams operation")
            with self._driver.session() as session:
                session.run(query, team=list_teams)
                self._logger.info("successfully create_teams operation")
        except ServiceUnavailable as exception:
            self._logger.error("{query} raised an error: \n {exception}"
                               .format(
                                   query=query, exception=exception))
            raise

    def create_players(self, list_players):
        self._logger.info("create_players")
        query = """
        UNWIND $players AS properties
        CREATE (n:Player)
        SET n = properties
        """
        try:
            self._logger.info("started create_players operation")
            with self._driver.session() as session:
                session.run(query, players=list_players)
            self._logger.info("successfully create_players operation")
        except ServiceUnavailable as exception:
            self._logger.error("{query} raised an error: \n {exception}"
                               .format(
                                   query=query, exception=exception))
            raise

    def player_playsIn_team(self):
        self._logger.info("player_playsIn_team")
        query = """
        MATCH (a:Player),(b:Team) WHERE a.team = b.id
        CREATE (a)-[r:playsIn]->(b)
        """
        try:
            self._logger.info("started player_playsIn_team operation")
            with self._driver.session() as session:
                session.run(query)
            self._logger.info("successfully player_playsIn_team operation")
        except ServiceUnavailable as exception:
            self._logger.error("{query} raised an error: \n {exception}"
                               .format(
                                   query=query, exception=exception))
            raise

    def create_league(self, list_leagues):
        self._logger.info("create_league")
        query = """
        UNWIND $league AS properties
        CREATE (n:League)
        SET n = properties
        """
        try:
            self._logger.info("started create_league operation")
            with self._driver.session() as session:
                session.run(query, leagues=list_leagues)
            self._logger.info("successfully create_league operation")
        except ServiceUnavailable as exception:
            self._logger.error("{query} raised an error: \n {exception}"
                               .format(
                                   query=query, exception=exception))
            raise

    def create_user(self, list_users):
        self._logger.info("create_user")
        query = """
        UNWIND $user AS properties
        CREATE (n:User)
        SET n = properties
        """
        try:
            self._logger.info("started create_user operation")
            with self._driver.session() as session:
                session.run(query, users=list_users)
            self._logger.info("successfully create_user operation")
        except ServiceUnavailable as exception:
            self._logger.error("{query} raised an error: \n {exception}"
                               .format(
                                   query=query, exception=exception))
            raise

    def create_user_and_leagues(self, user, list_leagues):
        self._logger.info("create_user_and_leagues")
        query = """
        CREATE (u:User ) set u = $user
        WITH u
        UNWIND $leagues AS league
        CREATE (u)-[:IN]->(l:League) set l = league
        """
        try:
            self._logger.info("started create_user_and_leagues operation")
            with self._driver.session() as session:
                session.run(query, user=user, leagues=list_leagues)
            self._logger.info("successfully create_user_and_leagues operation")
        except ServiceUnavailable as exception:
            self._logger.error("{query} raised an error: \n {exception}"
                               .format(
                                   query=query, exception=exception))
            raise

    def map_user_picks(self, user_id, gameweek_id, gameweek_picks):
        self._logger.info("map_user_picks")
        # gameweek_picks = map(json.dumps,gameweek_picks)
        query = """
        UNWIND $gameweek_picks as pick
        MATCH (p:Player) , (u:User) WHERE u.id = $user_id and
        p.id = pick.element
        MERGE (u)-[rel:OWN {gameweek_id:$gameweek_id }]->(p)
        ON CREATE SET rel= pick, rel.gameweek_id = $gameweek_id
        """
        try:
            self._logger.info("started map_user_picks operation")
            with self._driver.session() as session:
                session.run(query, user_id=user_id,
                            gameweek_id=gameweek_id,
                            gameweek_picks=gameweek_picks)
            self._logger.info("successfully map_user_picks operation")
        except ServiceUnavailable as exception:
            self._logger.error("{query} raised an error: \n {exception}"
                               .format(
                                   query=query, exception=exception))
            raise
