import aiohttp
from fplsupercharge.FplRequestApiHandler import FplRequestApiHandler
from fplsupercharge.datastore.neo4jDataStore import Datastore
import configparser


async def intialDataload():
    """
    return: creates a database that contain a list of players and teams
    """
    config = configparser.ConfigParser()
    config.read('tmp/FPLSUPERCHARGE.ini')
    username = config['INITILIAZATION']['username']
    password = config['INITILIAZATION']['password']
    db = Datastore()
    async with aiohttp.ClientSession() as session:
        fplRequestApiHandler = FplRequestApiHandler(session)
        # login
        await fplRequestApiHandler.login(username, password)
        # Get Teams and Store
        teams = await fplRequestApiHandler.get_teams(return_json=True)
        db.create_teams(teams)
        # Get Players and Store
        players = await fplRequestApiHandler.get_players(return_json=True)
        db.create_players(players)
        # players playsIn team
        db.player_playsIn_team()
        # Get me and league
        user = await fplRequestApiHandler.get_user(return_json=True)
        user_id = user['id']
        league_info = user.pop('leagues', None)
        db.create_user_and_leagues(user, league_info['classic'])
        # get my player pick for all the weeks
        picks = await fplRequestApiHandler.get_user_picks()
        for gameweek_id, pick in picks.items():
            db.map_user_picks(user_id, gameweek_id, pick)


if __name__ == "__main__":
    import asyncio
    asyncio.run(intialDataload())
