"""
Simple script to view snapshot data from MongoDB.
Useful for testing and debugging.
"""
from src.db.mongo_client import MongoDBClient
from datetime import datetime


def main():
    db_client = MongoDBClient()
    
    try:
        db_client.connect()
        
        # Get all snapshots
        snapshots = db_client.get_all_snapshots(limit=5)
        
        print(f"\n=== Last {len(snapshots)} Snapshots ===\n")
        
        for snapshot in snapshots:
            timestamp = snapshot['timestamp']
            game_count = snapshot['game_count']
            snapshot_id = snapshot['_id']
            
            # Calculate total playtime
            total_minutes = sum(game.get('playtime_forever', 0) 
                              for game in snapshot['games'])
            total_hours = round(total_minutes / 60, 2)
            
            print(f"ID: {snapshot_id}")
            print(f"Timestamp: {timestamp}")
            print(f"Games: {game_count}")
            print(f"Total Playtime: {total_hours} hours")
            print("-" * 50)
        
        # Show most played games from latest snapshot
        if snapshots:
            latest = snapshots[0]
            games = latest['games']
            
            # Sort by playtime
            sorted_games = sorted(
                games, 
                key=lambda g: g.get('playtime_forever', 0), 
                reverse=True
            )[:10]
            
            print(f"\n=== Top 10 Most Played Games ===\n")
            for i, game in enumerate(sorted_games, 1):
                name = game.get('name', 'Unknown')
                playtime_min = game.get('playtime_forever', 0)
                playtime_hrs = round(playtime_min / 60, 2)
                
                print(f"{i}. {name}")
                print(f"   Playtime: {playtime_hrs} hours")
            
    finally:
        db_client.close()


if __name__ == "__main__":
    main()
