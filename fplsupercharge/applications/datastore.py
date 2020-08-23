async def intialDataload(username: str, password: str,
                         db, fplRequestApiServices, logger) -> int:
    """
    return: creates a database that contain a list of players and teams
    """
    logger.info("delete all before")
    logger.info("loggin into FPL to retrieve data")
    await fplRequestApiServices.login(username, password)
    logger.info("Get Teams and Store")
    teams = await fplRequestApiServices.get_teams(return_json=True)
    db.create_teams(teams)
    logger.info("setting up fixture")
    fixtures = await fplRequestApiServices.get_fixtures(return_json=True)
    db.create_fixture(fixtures)
    logger.info("Get Players and Store")
    players = await fplRequestApiServices.get_players(return_json=True)
    db.create_players(players)
    logger.info("players playsIn team")
    db.player_playsIn_team()
    logger.info("Get me and the league i am in")
    user = await fplRequestApiServices.get_user(return_json=True)
    user_id = user['id']
    league_info = user.pop('leagues', None)
    if league_info['classic'] != None:
        db.create_user_and_leagues(user, league_info['classic'])
    logger.info("get my player pick for all the weeks")
    # picks = await fplRequestApiServices.get_user_picks() #FIXME: NoneType for User picks
    # for gameweek_id, pick in picks.items(): #FIXME: game_week_id is not set before the week. this needs to be in weekly
    #     db.map_user_picks(user_id, gameweek_id, pick)

async def weeklyUpdate(logger):
    # update FDR()
    # update fixture
    # update picks
    # update leagues
    # get user by leangues and update info
    raise NotImplementedError

async def createOrUpdateUserinfo(user_id: str, logger):
    raise NotImplementedError


async def createOrppdateLeagueInfo(league_id, logger):
    raise NotImplementedError
