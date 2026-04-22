"""
Entry point for running the Steam data ingestion pipeline.
This script can be triggered manually or via cron job.
"""
from src.clients.steam_client import SteamClient
from src.db.mongo_client import MongoDBClient
from src.services.ingestion_service import IngestionService


def main():
    """Run the data ingestion pipeline."""
    steam_client = SteamClient()
    db_client = MongoDBClient()
    
    try:
        db_client.connect()
        
        service = IngestionService(steam_client, db_client)
        result = service.run()
        
        return result
        
    except Exception as e:
        print(f"Error during ingestion: {e}")
        raise
    
    finally:
        db_client.close()


if __name__ == "__main__":
    main()
