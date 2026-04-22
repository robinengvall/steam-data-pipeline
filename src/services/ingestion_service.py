from src.clients.steam_client import SteamClient
from src.db.mongo_client import MongoDBClient


class IngestionService:
    
    def __init__(self, steam_client: SteamClient, db_client: MongoDBClient):
     
        self.steam_client = steam_client
        self.db_client = db_client
    
    def run(self):
      
        print("Starting data ingestion...")
        
        # Fetch data from Steam
        print("Fetching games from Steam API...")
        api_response = self.steam_client.get_owned_games()
        games = self.steam_client.extract_games(api_response)
        
        print(f"Retrieved {len(games)} games from Steam")
        
        # Store in database
        print("Saving snapshot to MongoDB...")
        snapshot_id = self.db_client.save_snapshot(games)
        
        # Generate summary
        total_playtime = sum(game.get("playtime_forever", 0) for game in games)
        
        summary = {
            "snapshot_id": snapshot_id,
            "game_count": len(games),
            "total_playtime_minutes": total_playtime,
            "total_playtime_hours": round(total_playtime / 60, 2)
        }
        
        print("\n=== Ingestion Complete ===")
        print(f"Snapshot ID: {summary['snapshot_id']}")
        print(f"Games stored: {summary['game_count']}")
        print(f"Total playtime: {summary['total_playtime_hours']} hours")
        
        return summary
