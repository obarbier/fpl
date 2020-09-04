"""
This Module focus on interacting with the data The goal is to try
to make this as transperant as possible. In future realease
we should be able to deside a database and the application
will store the data as needed
"""
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError
from utils.protosUtils import dict_to_protobuf
from protos.apiServices_pb2 import Team
import typing

# TODO: add decorator to remove dependencies on proto message
# TODO: allor protobuf to show default value


def to_neopropreties(dict: typing.Dict):
    # TODO: More usecase than just dict
    if(len(dict) != 0):
        return '{{ {} }}'.format(', '.join('{}: {}'.format(k, v)
                                           for k, v in dict.items()))


class Datastore:
    def __init__(self, uri, username, password, logger):
        try:
            self._logger = logger.getChild("neo4jservices")
            # FIXME: understand ssl/encrypted better
            self._driver = GraphDatabase.driver(
                uri=uri, auth=(username, password), encrypted=False)
            logger.info("succesfully logged into: {} ".format(uri))
        except AuthError as ex:
            logger.error(
                "Driver Error occured while initializing db {}".format(ex))
            raise

    def close(self):
        self._driver.close()

    def ready(self):
        query = """
        return "OK"
        """
        try:
            self._logger.info("started ready operation")
            with self._driver.session() as session:
                result = session.run(query)
                return result.single()
            self._logger.info("successfully ready operation")
        except ServiceUnavailable as exception:
            self._logger.error("{query} raised an error: \n {exception}"
                               .format(
                                   query=query, exception=exception))
            raise

    def deleteAll(self):
        query = """
        match (n)-[p]-(d) delete p,n,d
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
        CREATE (a)-[r:plays_for]->(b)
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

    def create_fixture(self, fixture_info: typing.List = {}):
        # properties = list(map(to_neopropreties, fixture_info))
        query = """
        UNWIND $fixture_info as fixture
        MATCH (h:Team) , (a:Team) WHERE h.id = fixture.team_h and
        a.id = fixture.team_a
        MERGE (h)-[rel:Plays]->(a)
        ON CREATE SET rel= fixture
        """
        try:
            with self._driver.session() as session:
                session.run(query, fixture_info=fixture_info)
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

    def get_teams(self):
        # TODO: show blank week/ double week
        # TODO: order by average 4 week difficulties
        # FIXME: DYNAMIC gameweek
        query = """
        Match (h:Team)-[rel:Plays]-(a:Team)
        where h.id <> a.id
        and rel.event in [1,2,3,4]
        return h as team_a,
        avg(rel.event) as avg_diff,
        collect(CASE h.id
        when rel.team_a THEN {game_week_id:rel.event,opp:a.short_name,
        diff: rel.team_a_difficulty}
        ELSE {game_week_id:rel.event,opp:a.short_name,
        diff: rel.team_h_difficulty}
        END )
        as fixture order by avg_diff
        """
        try:
            self._logger.info("started map_user_picks operation")
            res = []
            with self._driver.session() as session:
                result = session.run(query)
                for idx, record in enumerate(result):
                    teams, avg, fixtures = record.values()
                    team = Team()
                    dict_info = dict(teams.items())
                    dict_info['fixture'] = sorted(fixtures,
                                                  key=lambda fixture: fixture['game_week_id'])
                    dict_to_protobuf(dict_info, team)
                    res.append(team)
            return res
        except ServiceUnavailable as ex:
            self._logger.error("{query} raised an error: \n {exception}"
                               .format(
                                   query=query, exception=ex))
            raise

    def get_oneTeam(self, dict):
        query = """
        Match (h:Team {prop})-[rel:Plays]-(a:Team)
        where h.id <> a.id
        return h as team_a,
        collect(CASE h.id
        when rel.team_a THEN {game_week_id:rel.event,opp:a.short_name,
        diff: rel.team_a_difficulty}
        ELSE {game_week_id:rel.event,opp:a.short_name,
        diff: rel.team_h_difficulty}
        END )
        as fixture
        """
        properties = to_neopropreties(dict)
        query = query.format(prop=properties)
        print(query)
        try:
            self._logger.info("Processing the data for team with id {}"
                              .format(id))
            res = []
            with self._driver.session() as session:
                tx = session.begin_transaction()
                result = tx.run(query)
                for record in result:
                    res.append(record.get('p'))
                tx.commit()
                tx.close()
            return res
        except ServiceUnavailable as ex:
            self._logger.error("{query} raised an error: \n {exception}"
                               .format(
                                   query=query, exception=ex))
            raise

    def get_players(self):
        raise NotImplementedError
