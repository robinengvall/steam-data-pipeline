from flask import Blueprint, jsonify, request
from src.services.analytics_service import AnalyticsService
from src.clients.steam_client import SteamClient
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')


def create_routes(analytics_service: AnalyticsService):
    
    @api_bp.route('/stats', methods=['GET'])
    def get_stats():
        try:
            stats = analytics_service.get_overall_stats()
            return jsonify({
                "success": True,
                "data": stats
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @api_bp.route('/playtime/total', methods=['GET'])
    def get_total_playtime():
      
        try:
            playtime = analytics_service.get_total_playtime()
            return jsonify({
                "success": True,
                "data": playtime
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @api_bp.route('/playtime/history', methods=['GET'])
    def get_playtime_history():
        try:
            limit = request.args.get('limit', 10, type=int)
            history = analytics_service.get_playtime_history(limit=limit)
            return jsonify({
                "success": True,
                "data": history,
                "count": len(history)
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @api_bp.route('/playtime/deltas', methods=['GET'])
    def get_playtime_deltas():
        try:
            limit = request.args.get('limit', 10, type=int)
            deltas = analytics_service.get_playtime_deltas(limit=limit)
            return jsonify({
                "success": True,
                "data": deltas,
                "count": len(deltas)
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @api_bp.route('/games/top', methods=['GET'])
    def get_top_games():
        try:
            limit = request.args.get('limit', 10, type=int)
            games = analytics_service.get_most_played_games(limit=limit)
            return jsonify({
                "success": True,
                "data": games,
                "count": len(games)
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @api_bp.route('/games/new', methods=['GET'])
    def get_new_games():
        try:
            new_games = analytics_service.get_new_games()
            return jsonify({
                "success": True,
                "data": new_games,
                "count": len(new_games)
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @api_bp.route('/fetch-profile', methods=['GET'])
    def fetch_profile():
        try:
            steam_id = request.args.get('steam_id')
            
            if not steam_id:
                return jsonify({
                    "success": False,
                    "error": "Steam ID is required"
                }), 400
            
            steam_client = SteamClient(steam_id=steam_id)
            api_response = steam_client.get_owned_games(include_appinfo=True)
            games = steam_client.extract_games(api_response)
            
            if not games:
                return jsonify({
                    "success": False,
                    "error": "No games found. Profile might be private or Steam ID is invalid."
                }), 404
            
            total_playtime_minutes = sum(game.get('playtime_forever', 0) for game in games)
            total_playtime_hours = round(total_playtime_minutes / 60, 2)
            
            games_with_hours = []
            for game in games:
                playtime_minutes = game.get('playtime_forever', 0)
                playtime_hours = round(playtime_minutes / 60, 2)
                games_with_hours.append({
                    "appid": game.get('appid'),
                    "name": game.get('name', 'Unknown'),
                    "playtime_minutes": playtime_minutes,
                    "playtime_hours": playtime_hours,
                    "last_played": game.get('rtime_last_played', 0)
                })
            
            games_with_hours.sort(key=lambda x: x['playtime_hours'], reverse=True)
            
            return jsonify({
                "success": True,
                "data": {
                    "steam_id": steam_id,
                    "total_games": len(games),
                    "total_playtime_minutes": total_playtime_minutes,
                    "total_playtime_hours": total_playtime_hours,
                    "snapshot_timestamp": datetime.utcnow().isoformat(),
                    "games": games_with_hours
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    return api_bp
