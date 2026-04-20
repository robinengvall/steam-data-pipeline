import requests
import os
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")


BASE_URL = "https://api.steampowered.com" 


def get_ownded_games():
    url = f"{BASE_URL}/IPlayerService/GetOwnedGames/v1/"

    params = {
        "key":STEAM_API_KEY,
        "steamid":STEAM_ID,
        "include_appinfo":True
    }
    
    res = requests.get(url, params=params)
    res.raise_for_status()

    return res.json()


if __name__ == "__main__":
    data = get_ownded_games()
    games = data.get("response", {}).get("games", [])

    print(f"Found {len(games)} games\n")

    for game in games[:10]:
        name = game.get("name", "Unknown")
        playtime = game.get("playtime_forever", 0)
        last_played = game.get("rtime_last_played", 0)

        print(f"Name: {name}")
        print(f"Playtime: {playtime} min")
        print(f"Last played timestamp: {last_played}")
        print("-" * 30)
