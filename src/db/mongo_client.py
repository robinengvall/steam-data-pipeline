from pymongo import MongoClient, DESCENDING
from typing import Dict, List, Optional
from datetime import datetime
from config import Config


class MongoDBClient:
    """Client for interacting with MongoDB."""
    
    def __init__(self, uri: Optional[str] = None, db_name: Optional[str] = None):
        self.uri = uri or Config.MONGO_URI
        self.db_name = db_name or Config.MONGO_DB_NAME
        self.client = None
        self.db = None
    
    def connect(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        
        self.client.admin.command('ping')
        print(f"Connected to MongoDB: {self.db_name}")
    
    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed")
    
    def save_snapshot(self, games: List[Dict]):

        collection = self.db[Config.SNAPSHOTS_COLLECTION]
        
        snapshot = {
            "timestamp": datetime.utcnow(),
            "game_count": len(games),
            "games": games
        }
        
        result = collection.insert_one(snapshot)
        print(f"Snapshot saved with ID: {result.inserted_id}")
        return str(result.inserted_id)
    
    def get_latest_snapshot(self):

        collection = self.db[Config.SNAPSHOTS_COLLECTION]
        
        snapshot = collection.find_one(
            sort=[("timestamp", DESCENDING)]
        )
        
        return snapshot
    
    def get_all_snapshots(self, limit: Optional[int] = None):

        collection = self.db[Config.SNAPSHOTS_COLLECTION]
        
        cursor = collection.find().sort("timestamp", DESCENDING)
        
        if limit:
            cursor = cursor.limit(limit)
        
        return list(cursor)
