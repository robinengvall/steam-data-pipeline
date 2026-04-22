import requests
from typing import Dict, List, Optional
from config import Config


class SteamClient:
    """Client for interacting with the Steam Web API."""
    
    def __init__(self, api_key: Optional[str] = None, steam_id: Optional[str] = None):
        self.api_key = api_key or Config.STEAM_API_KEY
        self.steam_id = steam_id or Config.STEAM_ID
        self.base_url = Config.STEAM_API_BASE_URL
    
    def get_owned_games(self, include_appinfo: bool = True) -> Dict:
        """
        Fetch all games owned by the user.
        Returns raw API response as dictionary
        """
        url = f"{self.base_url}/IPlayerService/GetOwnedGames/v1/"
        
        params = {
            "key": self.api_key,
            "steamid": self.steam_id,
            "include_appinfo": include_appinfo,
            "format": "json"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
    
    def extract_games(self, api_response: Dict) -> List[Dict]:
        return api_response.get("response", {}).get("games", [])
