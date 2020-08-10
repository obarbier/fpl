API_BASE_URL = "https://fantasy.premierleague.com/api/"

API_URLS = {
    "dynamic": "/bootstrap-dynamic/",
    "fixtures": "/fixtures/",
    "gameweeks": "/events/",
    "gameweek_fixtures": "/fixtures/?event={/}",
    "gameweek_live": "/event/{/}/live",
    "league_classic": "/leagues-classic/{/}/standings/",
    "league_h2h": "/leagues-h2h/{/}/standings/",
    "league_h2h_fixtures": "/leagues-h2h-matches/league/{/}/?{/}page={/}",
    "players": "/elements/",
    "player": "/element-summary/{/}/",
    "settings": "/game-settings/",
    "static": "bootstrap-static/",
    "teams": "/teams/",
    "transfers": "/transfers/",
    "user": "/entry/{/}/",
    "user_cup": "/entry/{/}/cup/",
    "user_history": "/entry/{/}/history/",
    "user_picks": "/entry/{/}/event/{/}/picks/",
    "user_team": "/my-team/{/}/",
    "user_transfers": "/entry/{/}/transfers/",
    "user_latest_transfers": "/entry/{/}/transfers-latest/",
    "watchlist": "/watchlist/",
    "me": "/me/"
}
