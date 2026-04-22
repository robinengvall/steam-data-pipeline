from flask import Flask, jsonify, render_template
from src.db.mongo_client import MongoDBClient
from src.services.analytics_service import AnalyticsService
from src.routes.api_routes import create_routes


def create_app():
    app = Flask(__name__)
    
    db_client = MongoDBClient()
    db_client.connect()
    
    analytics_service = AnalyticsService(db_client)
    
    api_blueprint = create_routes(analytics_service)
    app.register_blueprint(api_blueprint)
    
    @app.route('/')
    def index():
        return render_template('dashboard.html')
    
    @app.route('/api')
    def api_info():
        return jsonify({
            "name": "Steam Data Pipeline API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "stats": "/api/stats",
                "playtime": {
                    "total": "/api/playtime/total",
                    "history": "/api/playtime/history?limit=10",
                    "deltas": "/api/playtime/deltas?limit=10"
                },
                "games": {
                    "top": "/api/games/top?limit=10",
                    "new": "/api/games/new"
                }
            }
        })
    
    @app.route('/health')
    def health():
        try:
            db_client.client.admin.command('ping')
            return jsonify({
                "status": "healthy",
                "database": "connected"
            }), 200
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }), 503
    
    app.db_client = db_client
    
    return app


def main():
    app = create_app()
    
    try:
        print("\nSteam Data Pipeline")
        print("Dashboard: http://localhost:5000")
        print("API Docs:  http://localhost:5000/api")
        print("\nPress CTRL+C to stop\n")
        
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    finally:
        if hasattr(app, 'db_client'):
            app.db_client.close()


if __name__ == '__main__':
    main()
