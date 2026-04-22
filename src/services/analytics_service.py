"""
Analytics service for processing game snapshot data.
Computes statistics, deltas, and insights from stored snapshots.
"""
from typing import List, Dict, Optional
from datetime import datetime


class AnalyticsService:
    """Service for analyzing game data from snapshots."""
    
    def __init__(self, db_client):
        self.db_client = db_client
    
    def get_overall_stats(self) -> Dict:
        latest = self.db_client.get_latest_snapshot()
        
        if not latest:
            return {
                "total_games": 0,
                "total_playtime_minutes": 0,
                "total_playtime_hours": 0,
                "snapshot_timestamp": None
            }
        
        games = latest['games']
        total_minutes = sum(game.get('playtime_forever', 0) for game in games)
        
        return {
            "total_games": len(games),
            "total_playtime_minutes": total_minutes,
            "total_playtime_hours": round(total_minutes / 60, 2),
            "snapshot_timestamp": latest['timestamp'].isoformat()
        }
    
    def get_total_playtime(self) -> Dict:
        latest = self.db_client.get_latest_snapshot()
        
        if not latest:
            return {
                "total_minutes": 0,
                "total_hours": 0,
                "game_count": 0
            }
        
        games = latest['games']
        total_minutes = sum(game.get('playtime_forever', 0) for game in games)
        
        return {
            "total_minutes": total_minutes,
            "total_hours": round(total_minutes / 60, 2),
            "game_count": len(games)
        }
    
    def get_playtime_history(self, limit: int = 10) -> List[Dict]:
        snapshots = self.db_client.get_all_snapshots(limit=limit)
        
        history = []
        for snapshot in reversed(snapshots):
            games = snapshot['games']
            total_minutes = sum(game.get('playtime_forever', 0) for game in games)
            
            history.append({
                "timestamp": snapshot['timestamp'].isoformat(),
                "total_playtime_hours": round(total_minutes / 60, 2),
                "total_playtime_minutes": total_minutes,
                "game_count": len(games)
            })
        
        return history
    
    def get_most_played_games(self, limit: int = 10) -> List[Dict]:
        latest = self.db_client.get_latest_snapshot()
        
        if not latest:
            return []
        
        games = latest['games']
        
        sorted_games = sorted(
            games,
            key=lambda g: g.get('playtime_forever', 0),
            reverse=True
        )[:limit]
        
        result = []
        for game in sorted_games:
            playtime_minutes = game.get('playtime_forever', 0)
            result.append({
                "appid": game.get('appid'),
                "name": game.get('name', 'Unknown'),
                "playtime_minutes": playtime_minutes,
                "playtime_hours": round(playtime_minutes / 60, 2),
                "last_played": game.get('rtime_last_played', 0)
            })
        
        return result
    
    def get_new_games(self) -> List[Dict]:
        snapshots = self.db_client.get_all_snapshots(limit=2)
        
        if len(snapshots) < 2:
            return []
        
        latest_games = {game['appid']: game for game in snapshots[0]['games']}
        previous_games = {game['appid'] for game in snapshots[1]['games']}
        
        new_game_ids = set(latest_games.keys()) - previous_games
        
        new_games = []
        for app_id in new_game_ids:
            game = latest_games[app_id]
            new_games.append({
                "appid": game.get('appid'),
                "name": game.get('name', 'Unknown'),
                "playtime_minutes": game.get('playtime_forever', 0),
                "playtime_hours": round(game.get('playtime_forever', 0) / 60, 2)
            })
        
        new_games.sort(key=lambda g: g['name'])
        
        return new_games
    
    def get_playtime_deltas(self, limit: int = 10) -> List[Dict]:
        snapshots = self.db_client.get_all_snapshots(limit=2)
        
        if len(snapshots) < 2:
            return []
        
        latest_games = {game['appid']: game for game in snapshots[0]['games']}
        previous_games = {game['appid']: game for game in snapshots[1]['games']}
        
        deltas = []
        for app_id, latest_game in latest_games.items():
            if app_id in previous_games:
                latest_playtime = latest_game.get('playtime_forever', 0)
                previous_playtime = previous_games[app_id].get('playtime_forever', 0)
                delta = latest_playtime - previous_playtime
                
                if delta > 0:
                    deltas.append({
                        "appid": app_id,
                        "name": latest_game.get('name', 'Unknown'),
                        "previous_playtime_minutes": previous_playtime,
                        "current_playtime_minutes": latest_playtime,
                        "delta_minutes": delta,
                        "delta_hours": round(delta / 60, 2)
                    })
        
        deltas.sort(key=lambda g: g['delta_minutes'], reverse=True)
        
        return deltas[:limit]
