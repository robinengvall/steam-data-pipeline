from flask import Blueprint, jsonify, request
from src.services.analytics_service import AnalyticsService

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
    
    return api_bp
